import unittest
import importlib.util
import tempfile
from pathlib import Path
from unittest.mock import patch

from importlib import metadata

from parsimony.analysis import token_diff
from parsimony.languages import extension_language, parse, structure, token_lines, track, unit_lines


HAS_LANGUAGES = all(importlib.util.find_spec(name) for name in
                    ('tree_sitter', 'tree_sitter_javascript', 'tree_sitter_typescript', 'tree_sitter_go'))


@unittest.skipUnless(HAS_LANGUAGES, 'install parsimony-benchmark[languages] for optional grammar tests')
class TreeSitterLanguageTests(unittest.TestCase):
    def test_track_and_extensions(self):
        self.assertIsNone(track("python"))
        with self.assertRaises(ValueError):
            track("rust")
        self.assertEqual(track("javascript")["unit_version"], "tree-sitter-units-v1")
        for path, language in (("x.js", "javascript"), ("x.jsx", "javascript"), ("x.mjs", "javascript"),
                               ("x.cjs", "javascript"), ("x.ts", "typescript"), ("x.tsx", "typescript"),
                               ("x.mts", "typescript"), ("x.cts", "typescript"), ("x.go", "go"), ("x.py", "python")):
            self.assertEqual(extension_language(path), language)
        self.assertIsNone(extension_language("x.rs"))

    def test_formatting_and_comments_are_no_token_diff(self):
        examples = [
            ("a.js", "const x=1;\n", "// note\nconst x = 1; // trailing\n"),
            ("a.ts", "function f(x:number):number{return x+1}\n", "// note\nfunction f ( x : number ) : number { return x + 1 }\n"),
            ("a.tsx", "const X=()=> <div>{name}</div>;\n", "// note\nconst X = () => <div>{ name }</div>;\n"),
            ("a.go", "package p\nfunc f(){x:=1;println(x)}\n", "package p\n// note\nfunc f() { x := 1; println(x) }\n"),
            ("a.js", "#!/usr/bin/env node\nconst x = 1;", "// note\nconst x = 1;"),
        ]
        for path, before, after in examples:
            with self.subTest(path=path):
                self.assertEqual(token_diff(token_lines(parse(before, path)), token_lines(parse(after, path))), (0, 0, False))
                self.assertEqual(token_diff(unit_lines(parse(before, path)), unit_lines(parse(after, path))), (0, 0, False))

    def test_container_literal_operator_and_type_changes_are_units(self):
        cases = (
            ("x.js", "const x = {};", "const x = [];"),
            ("x.js", 'const x = "";', 'const x = "text";'),
            ("x.js", "const x = a && b;", "const x = a || b;"),
            ("x.go", "package p\nfunc f(){ x := a; x = x + 1 }", "package p\nfunc f(){ x = <-ch; x = x &^ 1 }"),
            ("x.go", "package p\nfunc f(){ x += 1; x >>= 1 }", "package p\nfunc f(){ x -= 1; x <<= 1 }"),
            ("x.js", "let x = 1; x &&= true; x >>= 1;", "let x = 1; x ||= true; x >>>= 1;"),
            ("x.go", "package p\nfunc f(){ if x { return } }", "package p\nfunc f(){ if x { return }; if y { return } }"),
            ("x.ts", "const x: string = '';", "const x: number = '';"),
        )
        for path, before, after in cases:
            with self.subTest(path=path, before=before):
                a, b = parse(before, path), parse(after, path)
                self.assertNotEqual(token_diff(unit_lines(a), unit_lines(b))[:2], (0, 0))

    def test_anonymous_tokens_are_folded_into_units(self):
        units = unit_lines(parse("const x = a + b;", "x.js"))
        self.assertTrue(any("binary_expression[+]" in label for row in units for label in row))
        self.assertFalse(any(label.startswith("operator:") for row in units for label in row))

    def test_changes_affect_values_operators_and_modifiers(self):
        for path, before, after in (("x.js", "const x = a + 2;", "const y = a - 3;"),
                                    ("x.ts", "const x: Foo<T> = a;", "let x: Foo<T> = a;"),
                                    ("x.go", "package p\ntype T struct { X int }\n", "package p\ntype T struct { X string }\n")):
            a, b = parse(before, path), parse(after, path)
            self.assertNotEqual(token_diff(unit_lines(a), unit_lines(b))[:2], (0, 0))
        self.assertNotEqual(token_diff(unit_lines(parse("const x=1", "x.js")),
                                       unit_lines(parse("const x=2", "x.js")))[:2], (0, 0))

    def test_branching_nesting_and_grammar_examples(self):
        samples = [("x.js", "const x = value => value ? foo(value) : bar(value);"),
                   ("x.ts", "function f<T>(x: T): T { if (x) { return x; } return x; }"),
                   ("x.tsx", "const X = <T,>(p: T) => <div>{p}</div>;"),
                   ("x.go", 'package p\nimport "fmt"\ntype T struct { X int }\nfunc f(x int) { if x > 0 { fmt.Println(x) } }')]
        for path, source in samples:
            with self.subTest(path=path):
                parsed = parse(source, path)
                self.assertTrue(unit_lines(parsed))
                self.assertGreater(structure(parsed)[0], 0)
        flat = unit_lines(parse("if (x) { y(); }", "x.js"))
        nested = unit_lines(parse("if (x) { if (y) { y(); } }", "x.js"))
        self.assertGreater(sum(map(len, nested)), sum(map(len, flat)))

    def test_structure_has_function_baselines_and_boolean_decisions(self):
        one = structure(parse("function f(){ return a && b; }", "x.js"))[1]
        two = structure(parse("function f(){ if (a || b) return a && b; }", "x.js"))[1]
        self.assertEqual(one, 2)
        self.assertEqual(two, 4)

    def test_dependency_failures_have_install_guidance(self):
        def missing(name):
            if name == "tree-sitter-go":
                raise metadata.PackageNotFoundError(name)
            return "0.26.0"
        with patch("parsimony.languages.metadata.version", side_effect=missing):
            with self.assertRaisesRegex(ValueError, "pip install.*tree-sitter==0.26.0"):
                track("javascript")
        def wrong(name):
            return "0.0.0" if name == "tree-sitter-go" else "0.26.0"
        with patch("parsimony.languages.metadata.version", side_effect=wrong):
            with self.assertRaisesRegex(ValueError, "tree-sitter-go==0.25.0"):
                track("javascript")

    def test_large_tree_and_value_sensitive_literals(self):
        # More than 256 rows exercises native binding object lifetimes on Python 3.14.
        parsed = parse('const value = 1;\n' * 2000, 'x.js')
        self.assertEqual(len(token_lines(parsed)), 2000)
        self.assertEqual(len(unit_lines(parsed)), 2000)
        for before, after in [('const x = `hello`;', 'const x = `goodbye`;'),
                              ('const x = /ab/i;', 'const x = /ac/g;'),
                              ('const x = <div> </div>;', 'const x = <div></div>;')]:
            self.assertNotEqual(token_diff(unit_lines(parse(before, 'x.jsx')),
                                           unit_lines(parse(after, 'x.jsx')))[:2], (0, 0))

    def test_empty_and_invalid_syntax(self):
        for path in ("x.js", "x.tsx", "x.go"):
            self.assertEqual(unit_lines(parse("", path)), [])
        for path, source in (("x.js", "function {"), ("x.ts", "const x: = ;"), ("x.tsx", "<div>"), ("x.go", "func {")):
            with self.subTest(path=path), self.assertRaises(ValueError):
                parse(source, path)

    def test_pinned_typescript_grammar_rejects_published_base_constructs(self):
        # Vitest base: 647e6ade3b99523e3a0387a65fccfe918c331236,
        # packages/vitest/src/public/node.ts:209 (in scope); also
        # packages/vitest/optional-types.d.ts:4,7 (excluded corroboration).
        # Effect base: 9245bc59ebfa688e8c92dd691296ee69d0815e59,
        # packages/platform/src/HttpApiBuilder.ts (lines 910-937).
        fixtures = (
            'export type * as jsdomTypes from "jsdom";\n',
            "export const middleware: {\n"
            "  <E = never>(middleware: E): E\n"
            "  <R, E = never>(middleware: E, options: { withContext: true }): R\n"
            "} = (...args: any[]) => args[0];\n",
        )
        for source in fixtures:
            with self.subTest(source=source[:40]), self.assertRaisesRegex(
                ValueError, "invalid or recovered typescript syntax"
            ):
                parse(source, "fixture.ts")

    def test_never_executes_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'must-not-exist'
            parse(f'require("fs").writeFileSync("{marker}", "bad")', 'x.js')
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
