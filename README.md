# Mini Grep

A small, grep-inspired **filename search** tool in Python. It pairs an explicit
binary-search algorithm with a Textual terminal interface and a single-search CLI.
It does **not** search file contents or replace GNU grep.

## Overview

Index the immediate files of a chosen directory, search an exact name, and display
its path, size, and modification time. Names are case-sensitive; hidden files,
Unicode, all extensions, and quoted filenames with spaces are supported.

## Why this project exists

This project grew from Theory of Computation at Universidad de las Américas Puebla
(UDLAP). It connects formal-language recognition to a small application whose
algorithms, architecture, and filesystem behavior can be inspected and tested.
See [academic origin](docs/academic-origin.md) for evidence and historical limits.

## Features

- Exact filename lookup using binary search over a sorted snapshot.
- Textual TUI with visible directory, indexed count, refresh time, and clear errors.
- Manual refresh, help, and quit; Ctrl+R, F1, and Ctrl+Q shortcuts.
- CLI and TUI share the index, validation, search, and literal result rendering.
- Metadata rechecked on a match; unreadable entries produce visible warnings.

## Installation

Python **3.11+** is required. From a checkout of this repository:

```bash
git clone https://github.com/flaco332/grep-c.git
cd grep-c
python -m venv .venv
```

Activate on Linux/macOS:

```bash
source .venv/bin/activate
```

Activate in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
mini-grep
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` and
`.\.venv\Scripts\mini-grep.exe` directly; changing execution policy is unnecessary.

## Usage and demo

Use the original empty sample files for a quick demonstration:

```bash
mini-grep --directory programa
```

Inside the TUI:

```text
grep prueba.txt
grep "annual report.txt"
refresh
help
quit
```

`prueba.txt` is provided; `annual report.txt` illustrates quoting and is not a supplied
file. Search only the selected directory's immediate entries. New filenames need
refresh. A typical result for the included sample contains:

```text
FOUND
Name             prueba.txt
Size (bytes)     0
```

For one search without the UI:

```bash
mini-grep search prueba.txt --directory programa
python -m mini_grep search prueba.txt --directory programa
mini-grep --help
mini-grep --version
```

CLI exit codes: **0** found, **1** not found, **2** invalid input or filesystem error.
The old `python programa/grep_tui.py` launcher also works after installation and
indexes the process working directory unless `--directory` is provided.

## Academic origin: from formal language to software

```text
Formal language → DFA → BNF grammar → Lexer → Parser → Academic prototype
                                                       ↓
                                    Refactored architecture → Tested application
```

The academic model used a controlled `grep <pattern> <filename.txt>` syntax with a
restricted alphabet and deliberate recognition rules. Today's `grep <filename>`
syntax is a separate evolution. The original report/DFA is not in this repository;
the [formal-language document](docs/formal-language.md) labels reconstructed examples
explicitly. Current lexing uses `shlex`; there is no generated automata engine.

## Architecture and project structure

```text
src/mini_grep/
  parser.py       Lexing, syntax, filename validation
  index.py        Immutable file metadata and directory snapshots
  search.py       Binary search and live metadata verification
  app.py          Textual interaction
  cli.py          argparse and console entry point
  display.py      Shared literal Rich rendering
tests/            Core, filesystem, CLI, and headless TUI tests
docs/             Academic origin, grammar, architecture, release notes
programa/         Original samples and compatibility launcher
scripts/          Temporary-directory smoke benchmark
```

See [architecture](docs/architecture.md) for data flow, error contracts, and trade-offs.

## Algorithm and complexity

For `m` directory entries and `n` indexed regular files:

| Operation | Time |
| --- | --- |
| Scan, filter, collect metadata | O(m) |
| Sort indexed names | O(n log n) |
| Initial index / full refresh | O(m + n log n) |
| Lookup in the prepared snapshot | O(log n) |
| Successful lookup | O(log n) + one filesystem metadata read |

Space is O(m + n), including warning records. These bounds assume bounded filename
comparison costs; long strings add their comparison/hashing cost. CLI startup pays
the full indexing cost on each invocation. A hash set would offer average O(1)
membership; binary search stays as the single backend for its educational value.
[Performance notes](docs/performance.md) contain measured smoke checks, not speed claims.

## Testing and development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m pip check
python -m build
python -m pip_audit --local
python scripts/benchmark.py
```

Tests use temporary directories and Textual's headless Pilot. No standalone type
checker is configured. [Contributing](CONTRIBUTING.md) describes the small workflow.
For a repeatable validation environment, `requirements-dev.lock` records the tested
dependency versions; see [reproducibility](docs/reproducibility.md).

GitHub Actions checks Python 3.11/Linux and 3.13/Windows. Local verification covers
Windows with Python 3.11 and 3.13. macOS support is intended, not verified.

## How it differs from GNU grep

GNU grep searches patterns in file contents. Mini Grep searches **filenames only**.
It has no content patterns, regular expressions, recursion, glob expansion, or GNU
grep option compatibility. The academic command shape is historical context, not
a promise of GNU grep semantics.

## Limitations and roadmap

The index is a snapshot, not a filesystem transaction or watcher. Links to regular
files are followed and can expose target metadata outside the selected directory.
Filename comparison uses exact Unicode codepoints, even on case-insensitive filesystems.
Single-file metadata reads can be slow on network filesystems.

Potential future work: opt-in recursion or filename filters, then separately scoped
content search if useful. Regex support is deferred; no additional backend is planned.
See [GitHub metadata and screenshot guidance](docs/github-metadata.md).

## License

This project uses the [MIT License](LICENSE). Contributor attribution remains in
Git history; dependency licenses remain with their own distributions. See
[licensing](docs/licensing.md). Package version `0.1.0` has not been tagged or released.

[Public release review](PUBLIC_RELEASE_REVIEW.md) records the verification and
historical privacy finding. No history was rewritten; the separately documented
[anonymization plan](docs/privacy-history.md) remains unexecuted.
