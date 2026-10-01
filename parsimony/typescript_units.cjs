// Coding units for JavaScript and TypeScript from the official TypeScript parser.
//
// Line-delimited JSON over stdin/stdout: each request {path, source} gets one response.
// Syntax only: no type checking, module resolution, emit or execution of the parsed source.
'use strict';
const path = require('path');
const readline = require('readline');

const ts = require(require.resolve('typescript', {
  paths: [process.env.PARSIMONY_TYPESCRIPT_DIR || path.resolve(__dirname, '..')],
}));
const K = ts.SyntaxKind;
const NAMES = {};
for (const [name, value] of Object.entries(K)) {
  if (!(value in NAMES) && !/^(First|Last)/.test(name)) NAMES[value] = name;
}

const SCRIPT_KINDS = {
  '.ts': ts.ScriptKind.TS, '.mts': ts.ScriptKind.TS, '.cts': ts.ScriptKind.TS, '.tsx': ts.ScriptKind.TSX,
  '.js': ts.ScriptKind.JS, '.mjs': ts.ScriptKind.JS, '.cjs': ts.ScriptKind.JS, '.jsx': ts.ScriptKind.JSX,
};
// Names and literals keep their value; these token kinds are units, not folded punctuation.
const VALUE_KINDS = new Set([K.Identifier, K.PrivateIdentifier, K.StringLiteral, K.NumericLiteral, K.BigIntLiteral,
  K.RegularExpressionLiteral, K.NoSubstitutionTemplateLiteral, K.TemplateHead, K.TemplateMiddle, K.TemplateTail,
  K.JsxText]);
const KEYWORD_UNITS = new Set([K.TrueKeyword, K.FalseKeyword, K.NullKeyword, K.ThisKeyword, K.SuperKeyword,
  K.AnyKeyword, K.BigIntKeyword, K.BooleanKeyword, K.IntrinsicKeyword, K.NeverKeyword, K.NumberKeyword,
  K.ObjectKeyword, K.StringKeyword, K.SymbolKeyword, K.UndefinedKeyword, K.UnknownKeyword, K.VoidKeyword]);
// Pure syntax containers and expression wrappers do not represent useful units.
const WRAPPERS = new Set([K.SourceFile, K.ExpressionStatement, K.ParenthesizedExpression, K.ParenthesizedType,
  K.TemplateSpan, K.TemplateLiteralTypeSpan, K.ImportClause, K.NamedImports, K.NamedExports, K.JsxExpression,
  K.CaseBlock]);
// Each block ends with an EndBlock unit, so nesting and moving code across blocks count.
const BLOCKS = new Set([K.Block, K.ModuleBlock, K.CaseBlock, K.ClassDeclaration, K.ClassExpression]);
const BRANCHES = new Set([K.IfStatement, K.ConditionalExpression, K.CaseClause, K.ForStatement, K.ForInStatement,
  K.ForOfStatement, K.WhileStatement, K.DoStatement, K.CatchClause]);
const FUNCTIONS = new Set([K.FunctionDeclaration, K.FunctionExpression, K.ArrowFunction, K.MethodDeclaration,
  K.Constructor, K.GetAccessor, K.SetAccessor]);
const PUNCTUATION = new Set([K.OpenParenToken, K.CloseParenToken, K.OpenBraceToken, K.CloseBraceToken,
  K.OpenBracketToken, K.CloseBracketToken, K.CommaToken, K.SemicolonToken, K.DotToken, K.EndOfFileToken]);

const isToken = (node) => node.kind >= K.FirstToken && node.kind <= K.LastToken;
const folded = (node) => isToken(node) && !VALUE_KINDS.has(node.kind) && !KEYWORD_UNITS.has(node.kind);
const tokenText = (kind) => ts.tokenToString(kind) || NAMES[kind];

function children(node) {
  const out = [];
  ts.forEachChild(node, (child) => { out.push(child); });
  return out;
}

function declarationKind(list) {
  const flags = list.flags;
  if ((flags & ts.NodeFlags.AwaitUsing) === ts.NodeFlags.AwaitUsing) return 'await using';
  if (flags & ts.NodeFlags.Using) return 'using';
  if (flags & ts.NodeFlags.Const) return 'const';
  if (flags & ts.NodeFlags.Let) return 'let';
  return 'var';
}

// Operators, modifiers and keywords become part of their parent's label.
function terminals(node) {
  const out = children(node).filter(folded).map((child) => tokenText(child.kind));
  if (node.kind === K.PrefixUnaryExpression || node.kind === K.PostfixUnaryExpression || node.kind === K.TypeOperator) {
    out.push(tokenText(node.operator));
  }
  if (node.kind === K.HeritageClause) out.push(tokenText(node.token));
  if (node.kind === K.MetaProperty) out.push(tokenText(node.keywordToken));
  if (node.kind === K.VariableStatement || (node.kind === K.VariableDeclarationList && node.parent.kind !== K.VariableStatement)) {
    out.push(declarationKind(node.kind === K.VariableStatement ? node.declarationList : node));
  }
  if (node.isTypeOnly) out.push('type');
  if (node.kind === K.ImportDeclaration && node.importClause && node.importClause.isTypeOnly) out.push('type');
  if (node.kind === K.ExportAssignment && node.isExportEquals) out.push('=');
  return out;
}

function label(node, keepValues) {
  let text = NAMES[node.kind];
  if (keepValues && VALUE_KINDS.has(node.kind)) text += ':' + node.text;
  const extra = terminals(node);
  return extra.length ? `${text}[${extra.join(',')}]` : text;
}

function wrapper(node) {
  return WRAPPERS.has(node.kind) ||
    (node.kind === K.VariableDeclarationList && node.parent.kind === K.VariableStatement) ||
    // JSX drops whitespace-only text that contains a line break: it is formatting.
    (node.kind === K.JsxText && node.containsOnlyTriviaWhiteSpaces && /[\r\n]/.test(node.text));
}

function walk(sf) {
  const row = (pos) => sf.getLineAndCharacterOfPosition(pos).line;
  const units = [], plain = [];
  let count = 0, branches = 0;
  const stack = [sf];
  while (stack.length) {
    const node = stack.pop();
    if (node.end_marker) {
      units.push([node.row, 'EndBlock']);
      plain.push([node.row, 'EndBlock']);
      continue;
    }
    if (folded(node)) continue;
    if (!wrapper(node)) {
      const at = row(node.getStart(sf));
      units.push([at, label(node, true)]);
      plain.push([at, label(node, false)]);
      count += 1;
      if (FUNCTIONS.has(node.kind) || BRANCHES.has(node.kind)) branches += 1;
      if (node.kind === K.BinaryExpression &&
          (node.operatorToken.kind === K.AmpersandAmpersandToken || node.operatorToken.kind === K.BarBarToken)) {
        branches += 1;
      }
    }
    if (BLOCKS.has(node.kind)) stack.push({end_marker: true, row: row(node.end)});
    // A literal is one value-sensitive unit; its children (if any) are not separate units.
    if (!VALUE_KINDS.has(node.kind)) stack.push(...children(node).reverse());
  }
  return {units, plain, structure: [count, branches]};
}

// Significant lexical leaves (a diagnostic, like the Python token metrics).
function tokens(sf) {
  const out = [];
  const stack = [sf];
  while (stack.length) {
    const node = stack.pop();
    if (node.kind >= K.FirstJSDocNode && node.kind <= K.LastJSDocNode) continue;
    const kids = node.getChildren(sf);
    if (kids.length === 0 && isToken(node)) {
      if (!PUNCTUATION.has(node.kind)) {
        out.push([sf.getLineAndCharacterOfPosition(node.getStart(sf)).line, `${NAMES[node.kind]}:${node.getText(sf)}`]);
      }
      continue;
    }
    stack.push(...kids.slice().reverse());
  }
  return out;
}

function analyze(file, source) {
  const ext = path.extname(file).toLowerCase();
  const kind = SCRIPT_KINDS[ext];
  if (kind === undefined) throw new Error(`unsupported source path: ${file}`);
  const name = 'input' + ext;
  const sf = ts.createSourceFile(name, source, ts.ScriptTarget.Latest, true, kind);
  // A program with this one file reports parse errors plus TypeScript-only syntax in JavaScript files.
  const host = {
    getSourceFile: (f) => (f === name ? sf : undefined), fileExists: (f) => f === name,
    readFile: (f) => (f === name ? source : undefined), getDefaultLibFileName: () => 'lib.d.ts',
    writeFile: () => {}, getCurrentDirectory: () => '', getCanonicalFileName: (f) => f,
    useCaseSensitiveFileNames: () => true, getNewLine: () => '\n', getDirectories: () => [],
  };
  const program = ts.createProgram({rootNames: [name], host,
    options: {allowJs: true, noLib: true, noResolve: true, types: [], jsx: ts.JsxEmit.Preserve}});
  const diagnostics = program.getSyntacticDiagnostics(sf);
  if (diagnostics.length) {
    const d = diagnostics[0];
    const line = sf.getLineAndCharacterOfPosition(d.start).line + 1;
    return {ok: false, error: `${file}:${line}: ${ts.flattenDiagnosticMessageText(d.messageText, ' ')}`};
  }
  return {ok: true, ...walk(sf), tokens: tokens(sf)};
}

if (require.main === module) {
  process.stdout.write(JSON.stringify({ready: true, typescript: ts.version}) + '\n');
  const lines = readline.createInterface({input: process.stdin, crlfDelay: Infinity});
  lines.on('line', (line) => {
    let response;
    try {
      const {path: file, source} = JSON.parse(line);
      response = analyze(file, source);
    } catch (error) {
      response = {ok: false, fatal: true, error: String(error && error.stack || error)};
    }
    process.stdout.write(JSON.stringify(response) + '\n');
  });
}

module.exports = {analyze};
