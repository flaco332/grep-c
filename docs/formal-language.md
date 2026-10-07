# Formal language and command parsing

## Academic model

The project owner's description supplies the original command shape and deliberate
restrictions. No complete report or original automaton is available in the Git
objects reviewed. The following BNF is an **illustrative reconstruction** of that
description, not a verified transcription of the original grammar:

```bnf
<Command>     ::= "grep" " " <Pattern> " " <Filename>
<Pattern>     ::= <PatternChar> | <PatternChar><Pattern>
<PatternChar> ::= <Letter> | <Digit> | "_" | "-"
<Filename>    ::= <NameBody> ".txt"
<NameBody>    ::= <PatternChar> | <PatternChar><NameBody>
<Letter>      ::= "a" | ... | "z" | "A" | ... | "Z"
<Digit>       ::= "0" | ... | "9"
```

The exact letter alphabet and `<NameBody>` productions above are explanatory
assumptions; confirm them against the original report before citing them as its
precise definition. A literal single space is shown as part of the rigid model.

This restricted language is regular. A DFA can recognize the fixed keyword,
required separators, nonempty character groups, and suffix using finite states.
Its conceptual phases are:

```text
start → read "grep" → space → nonempty pattern → space
      → nonempty filename body → read ".txt" → accept at end of input
```

An invalid symbol, missing component, or extra trailing text leads to rejection.
This is a conceptual explanation, not the original state-transition diagram.
The grammar states the allowed structure; lexical analysis recognizes components;
syntactic analysis verifies their arrangement. Recognition alone does not imply
searching contents or implementing regular-expression semantics.

## Implemented command language

The current TUI has a different, intentionally small grammar:

```bnf
<Command> ::= "grep" <Whitespace> <FilenameToken>
            | "refresh"
            | "help"
            | "quit"
```

Leading and trailing whitespace are accepted. Between tokens, spaces or tabs are
accepted. Keywords are lowercase and case-sensitive. `shlex.split` with POSIX
quoting and comments disabled produces tokens. Single or double quotes group
filenames with spaces; normal shlex escape rules apply. `#` is a literal filename
character, not a comment. Shell expansion, pipes, redirection, command substitution,
and execution are never performed. A literal filename can contain shell-looking
characters; they do not become commands.

The parser validates the command keyword, argument count, and filename. A filename
must be a nonempty basename other than `.` or `..`, with no `/`, `\`, or control
characters. Names need no extension; matching preserves case and Unicode codepoints
without normalization. Filename restrictions are application rules, not a complete
portable filesystem filename validator: each OS still determines what names exist.

```text
grep file.txt                valid
grep "annual report.pdf"     valid
grep canción.txt             valid
grep                        missing_argument
grep file.txt extra          too_many_arguments
GREP file.txt                unknown_command
grep "unfinished             invalid_syntax
grep ../file.txt             invalid_filename
```

Empty input has the separate `empty_command` code. Tests assert each error category.
The CLI receives tokens from the user's shell through `argparse`; it reuses the
same filename validation and search engine rather than reconstructing a TUI string.

References: [Python shlex](https://docs.python.org/3/library/shlex.html) explains the
lexing and quoting rules. The current project contains an explicit small parser,
not a generated DFA or a compiler frontend.
