import unittest
import importlib.util
import tempfile
from pathlib import Path
from unittest.mock import patch

from importlib import metadata

from parsimony.analysis import token_diff
from parsimony.languages import extension_language, parse, structure, token_lines, track, unit_lines


HAS_GO = all(importlib.util.find_spec(name) for name in ('tree_sitter', 'tree_sitter_go'))


def _has_typescript():
    try:
        track('typescript')
        return True
    except ValueError:
        return False


HAS_TYPESCRIPT = _has_typescript()
HAS_LANGUAGES = HAS_GO and HAS_TYPESCRIPT


def units(source, path):
    return unit_lines(parse(source, path))


def labels(source, path):
    return [label for row in units(source, path) for label in row]


class ExtensionTests(unittest.TestCase):
    def test_extensions_and_unsupported_tracks(self):
        self.assertIsNone(track("python"))
        with self.assertRaises(ValueError):
            track("rust")
        for path, language in (("x.js", "javascript"), ("x.jsx", "javascript"), ("x.mjs", "javascript"),
                               ("x.cjs", "javascript"), ("x.ts", "typescript"), ("x.tsx", "typescript"),
                               ("x.mts", "typescript"), ("x.cts", "typescript"), ("x.go", "go"), ("x.py", "python")):
            self.assertEqual(extension_language(path), language)
        self.assertIsNone(extension_language("x.rs"))


@unittest.skipUnless(HAS_TYPESCRIPT, 'run `npm ci` (Node.js + pinned typescript) for JavaScript/TypeScript tests')
class TypeScriptCompilerTests(unittest.TestCase):
    def test_track_identity(self):
        for language in ("javascript", "typescript"):
            self.assertEqual(track(language), {"language": language, "unit_version": "typescript-compiler-units-v1",
                                               "versions": {"typescript": "5.9.3"}})

    def test_formatting_and_comments_are_no_diff(self):
        examples = [
            ("a.js", "const x=1;\n", "// note\nconst x = 1; // trailing\n"),
            ("a.ts", "function f(x:number):number{return x+1}\n", "// note\nfunction f ( x : number ) : number { return x + 1 }\n"),
            ("a.tsx", "const X=()=> <div>{name}</div>;\n", "// note\nconst X = () => <div>{ name }</div>;\n"),
            ("a.tsx", "const X = () => <div><b /></div>;\n", "const X = () => (\n  <div>\n    <b />\n  </div>\n);\n"),
            ("a.js", "#!/usr/bin/env node\nconst x = 1;", "// note\nconst x = 1;"),
            ("a.ts", "const s = 'a';", 'const s = "a";'),
            ("a.ts", "/** doc */\nfunction f() {}", "function f() {}"),
        ]
        for path, before, after in examples:
            with self.subTest(path=path, after=after):
                self.assertEqual(token_diff(units(before, path), units(after, path)), (0, 0, False))
        self.assertEqual(token_diff(token_lines(parse("const x=1;", "a.js")),
                                    token_lines(parse("// c\nconst x = 1;", "a.js"))), (0, 0, False))

    def test_container_literal_operator_and_type_changes_are_units(self):
        cases = (
            ("x.js", "const x = {};", "const x = [];"),
            ("x.js", 'const x = "";', 'const x = "text";'),
            ("x.js", "const x = a && b;", "const x = a || b;"),
            ("x.js", "let x = 1; x &&= true; x >>= 1;", "let x = 1; x ||= true; x >>>= 1;"),
            ("x.js", "x++;", "x--;"),
            ("x.ts", "const x: string = '';", "const x: number = '';"),
            ("x.ts", "const x: Foo<T> = a;", "let x: Foo<T> = a;"),
            ("x.ts", "export const x = 1;", "const x = 1;"),
            ("x.ts", "import { A } from 'a';", "import type { A } from 'a';"),
            ("x.ts", "type K = keyof T;", "type K = readonly T[];"),
            ("x.ts", "class A extends B {}", "class A implements B {}"),
        )
        for path, before, after in cases:
            with self.subTest(before=before):
                self.assertNotEqual(token_diff(units(before, path), units(after, path))[:2], (0, 0))

    def test_anonymous_tokens_are_folded_into_units(self):
        found = labels("const x = a + b;", "x.js")
        self.assertIn("BinaryExpression[+]", found)
        self.assertIn("VariableStatement[const]", found)
        self.assertFalse(any(label.startswith(("PlusToken", "EqualsToken", "ConstKeyword")) for label in found))
        self.assertEqual(labels("export const x = 1;", "x.ts")[0], "VariableStatement[export,const]")
        self.assertEqual(labels("if (x) { y(); }", "x.js"),
                         ["IfStatement", "Identifier:x", "Block", "CallExpression", "Identifier:y", "EndBlock"])

    def test_values_and_nesting(self):
        self.assertNotEqual(token_diff(units("const x=1", "x.js"), units("const x=2", "x.js"))[:2], (0, 0))
        flat = units("if (x) { y(); }", "x.js")
        nested = units("if (x) { if (y) { y(); } }", "x.js")
        self.assertGreater(sum(map(len, nested)), sum(map(len, flat)))
        for before, after in [('const x = `hello`;', 'const x = `goodbye`;'),
                              ('const x = /ab/i;', 'const x = /ac/g;'),
                              ('const x = <div> </div>;', 'const x = <div></div>;')]:
            self.assertNotEqual(token_diff(units(before, 'x.jsx'), units(after, 'x.jsx'))[:2], (0, 0))
        # Identifier/literal-insensitive units ignore renames but not structure.
        a, b = parse("const x = f(1);", "x.ts"), parse("const y = g(2);", "x.ts")
        self.assertEqual(token_diff(unit_lines(a, False), unit_lines(b, False))[:2], (0, 0))

    def test_structure_has_function_baselines_and_boolean_decisions(self):
        self.assertEqual(structure(parse("function f(){ return a && b; }", "x.js"))[1], 2)
        self.assertEqual(structure(parse("function f(){ if (a || b) return a && b; }", "x.js"))[1], 4)
        self.assertGreater(structure(parse("const x = 1;", "x.ts"))[0], 0)

    def test_modern_typescript_rejected_by_the_old_grammar(self):
        # Valid constructs that tree-sitter-typescript 0.23.2 rejected, all from published
        # DeepSWE base files or patches (docs/typescript-parser-investigation.md).
        fixtures = {
            # vitest 647e6ade packages/vitest/src/public/node.ts:209; meriyah src/meriyah.ts:36
            'type-only namespace re-export': 'export type * as Vite from "vite";\n',
            # ofetch src/index.ts:6
            'type-only star re-export': 'export type * from "./types.ts";\n',
            # Effect 9245bc59 packages/platform/src/HttpApi.ts:47-50
            'variance annotations': 'export interface Api<out Id extends string, in out E = never> { id: Id }\n',
            # Effect packages/platform/src/HttpApiBuilder.ts:910-937 and kea src/types.ts:68-74
            'generic call signatures on new lines': (
                "export const middleware: {\n"
                "  <E = never>(middleware: E): Layer<E>\n"
                "  <R, E = never>(middleware: E, options: { withContext: true }): R\n"
                "} = (...args: any[]) => args[0];\n"
                "interface Wrapper {\n  inputs: (A | B)[] // note\n  <T>(props: T): T\n  (): void\n}\n"),
            # dynamodb-toolbox src/schema/actions/parseCondition/condition.ts:120-124
            'property named in': "type InCondition<P> = {\n  attr: P\n  in: P[]\n}\n",
            # koota, kysely, drizzle and others: inline import types
            'import type arrays': "const xs: import('./types').Aspect[] = [];\nlet y: import('./a').B<C>['d'];\n",
            # arktype ark/json-schema/json.ts
            'namespace member in parenthesized type': "let validators: (type.Any | undefined)[];\n",
            # meriyah src/parser.ts and koota predicate.ts
            'contextual keywords as names': "let satisfies = false;\nif (using.flags) {}\n",
            # drizzle-orm window functions
            'generic tagged template': "const s = sql<(T extends A ? T['_'] : string) | null>`min(${e})`;\n",
        }
        for name, source in fixtures.items():
            with self.subTest(name):
                self.assertTrue(units(source, 'fixture.ts'))

    def test_empty_and_invalid_syntax(self):
        for path in ("x.js", "x.ts", "x.tsx"):
            self.assertEqual(units("", path), [])
        for path, source in (("x.js", "function {"), ("x.ts", "const x: = ;"), ("x.tsx", "<div>"),
                             ("x.ts", "const x = { a: 1 b: 2 };"), ("x.ts", "type T = Foo<;"),
                             # TypeScript-only syntax is invalid in JavaScript files.
                             ("x.js", "const x: number = 1;"), ("x.js", "interface A {}"),
                             # Invalid edits seen in published patches.
                             ("x.ts", "const o = { ...a, b: c, };\n}\n"), ("x.ts", "f(a b);")):
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "invalid or recovered"):
                parse(source, path)
        with self.assertRaisesRegex(ValueError, r"x\.ts:2: "):
            parse("const a = 1;\nconst x: = ;", "x.ts")

    def test_large_file(self):
        parsed = parse('const value = 1;\n' * 2000 + 'const s = ' + ' + '.join(['"a"'] * 5000) + ';\n', 'x.js')
        self.assertEqual(len(unit_lines(parsed)), 2001)
        self.assertEqual(len(token_lines(parsed)), 2001)

    def test_unicode_source(self):
        self.assertIn("StringLiteral:héllo ✓", labels("const s = 'héllo ✓';", "x.ts"))

    def test_never_executes_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'must-not-exist'
            parse(f'require("fs").writeFileSync("{marker}", "bad")', 'x.js')
            self.assertFalse(marker.exists())


@unittest.skipUnless(HAS_GO, 'install parsimony-benchmark[languages] for Go grammar tests')
class GoTreeSitterTests(unittest.TestCase):
    def test_track_identity(self):
        self.assertEqual(track("go"), {"language": "go", "unit_version": "tree-sitter-units-v1",
                                       "versions": {"tree-sitter": "0.26.0", "tree-sitter-go": "0.25.0"}})

    def test_formatting_and_comments_are_no_diff(self):
        before, after = "package p\nfunc f(){x:=1;println(x)}\n", "package p\n// note\nfunc f() { x := 1; println(x) }\n"
        self.assertEqual(token_diff(token_lines(parse(before, "a.go")), token_lines(parse(after, "a.go"))), (0, 0, False))
        self.assertEqual(token_diff(units(before, "a.go"), units(after, "a.go")), (0, 0, False))

    def test_changes_are_units(self):
        for before, after in (("package p\nfunc f(){ x := a; x = x + 1 }", "package p\nfunc f(){ x = <-ch; x = x &^ 1 }"),
                              ("package p\nfunc f(){ x += 1; x >>= 1 }", "package p\nfunc f(){ x -= 1; x <<= 1 }"),
                              ("package p\nfunc f(){ if x { return } }", "package p\nfunc f(){ if x { return }; if y { return } }"),
                              ("package p\ntype T struct { X int }\n", "package p\ntype T struct { X string }\n")):
            with self.subTest(before=before):
                self.assertNotEqual(token_diff(units(before, "x.go"), units(after, "x.go"))[:2], (0, 0))
        parsed = parse('package p\nimport "fmt"\ntype T struct { X int }\nfunc f(x int) { if x > 0 { fmt.Println(x) } }', "x.go")
        self.assertTrue(unit_lines(parsed))
        self.assertGreater(structure(parsed)[0], 0)

    def test_dependency_failures_have_install_guidance(self):
        def missing(name):
            if name == "tree-sitter-go":
                raise metadata.PackageNotFoundError(name)
            return "0.26.0"
        with patch("parsimony.languages.metadata.version", side_effect=missing):
            with self.assertRaisesRegex(ValueError, "pip install.*tree-sitter==0.26.0"):
                track("go")
        def wrong(name):
            return "0.0.0" if name == "tree-sitter-go" else "0.26.0"
        with patch("parsimony.languages.metadata.version", side_effect=wrong):
            with self.assertRaisesRegex(ValueError, "tree-sitter-go==0.25.0"):
                track("go")

    def test_large_tree_empty_and_invalid(self):
        # More than 256 rows exercises native binding object lifetimes on Python 3.14.
        parsed = parse('package p\n' + 'var value = 1\n' * 2000, 'x.go')
        self.assertEqual(len(token_lines(parsed)), 2001)
        self.assertEqual(unit_lines(parse("", "x.go")), [])
        with self.assertRaises(ValueError):
            parse("func {", "x.go")


if __name__ == "__main__":
    unittest.main()
