// Static syntax-only helper. Build this file alone outside target repositories.
// It never resolves imports, type-checks, emits or executes submitted code.
package main

import (
	"encoding/json"
	"go/parser"
	"go/scanner"
	"go/token"
	"os"
	"runtime"
)

type diagnostic struct {
	Line    int    `json:"line"`
	Column  int    `json:"column"`
	Offset  int    `json:"offset"`
	Message string `json:"message"`
}

func main() {
	if len(os.Args) != 2 {
		panic("expected one source path")
	}
	fset := token.NewFileSet()
	_, err := parser.ParseFile(fset, os.Args[1], nil, parser.AllErrors|parser.ParseComments|parser.SkipObjectResolution)
	diagnostics := []diagnostic{}
	if err != nil {
		if list, ok := err.(scanner.ErrorList); ok {
			for _, e := range list {
				diagnostics = append(diagnostics, diagnostic{e.Pos.Line, e.Pos.Column, e.Pos.Offset, e.Msg})
			}
		} else {
			panic(err)
		}
	}
	json.NewEncoder(os.Stdout).Encode(struct {
		OK          bool         `json:"ok"`
		Version     string       `json:"version"`
		Diagnostics []diagnostic `json:"diagnostics"`
	}{err == nil, runtime.Version(), diagnostics})
}
