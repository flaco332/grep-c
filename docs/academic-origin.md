# Academic origin

Mini Grep began as a Theory of Computation project at Universidad de las Américas
Puebla (UDLAP). Its purpose was to connect a formal language to executable software:

```text
Formal language → DFA → BNF grammar → Lexer → Parser → Academic prototype
                                                       ↓
                                  Refactored, tested filename-search application
```

## Scope and evidence

The academic context in this document comes from the project owner's description.
The original report and its complete implementation are **not present in this
checkout or its locally available Git history**. This is a summary, not a claim
that the repository contains the original DFA, generated lexer, or parser generator.

The original controlled language used a lowercase keyword and a shape such as:

```text
grep <pattern> <filename.txt>
```

Its restricted alphabet, limited patterns, `.txt` suffix, and rigid spacing were
deliberate constraints of the formal model. The academic work emphasized command
recognition, structural validation, filename matching, and explanatory errors.
It was not intended to reproduce GNU grep.

## From language recognition to software

- **Formal language:** define which strings are admissible commands.
- **DFA:** consume symbols and accept only strings that reach an accepting state.
- **Grammar:** describe the command structure in productions.
- **Lexer:** recognize the keyword, pattern, filename, and separators.
- **Parser:** check their order and required structure.
- **Application:** connect a recognized command to the supported operation.

These are related views of the language, not necessarily generated artifacts in
the current codebase. [Formal language](formal-language.md) illustrates the model
and distinguishes it from the command grammar implemented today.

## Evolution visible in Git

Early commits created **empty** C source files, an empty Makefile, and an empty
`docs/reporte.md`. A historical README described content search and linked lists,
but none of those C files contained executable code. That text is evidence of a
proposal, not implemented functionality, and its course label differs from the
academic context supplied by the owner.

Commit `22be562` introduced the Python Textual application and removed the empty
scaffold. Commit `9a6ead7` moved it into `programa/` and added six empty sample
files. The version at baseline `ae2b9a0` accepted `grep <filename>` and searched
exact filenames using binary search over a sorted directory listing.

## Current implementation

The current package preserves exact, case-sensitive filename lookup and binary
search. It adds independently testable modules, explicit syntax errors, metadata
models, manual refresh, directory selection, and a small CLI.

It supports all extensions, hidden files, Unicode, and quoted names with spaces.
Its parser uses Python's `shlex` as a lexer followed by explicit structural checks;
it does not run a shell or enforce the original academic alphabet and `.txt` rule.
It does not search file contents. These extensions belong to the software's
current implementation and must not be attributed to the original prototype.
