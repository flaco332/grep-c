# Public release review

Audit date: **2026-10-06**. Scope: this existing repository and all locally available
Git refs/objects. Work branch: **`feat/professional-public-release`**, created from
`ae2b9a0` before tracked application changes. No second project or checkout was
created. Virtual environments and ignored build artifacts stay in this directory.

## Initial state

- Clean `main` at `ae2b9a05443c386ed7bb7fc7cba53b30dda0fb1c`; seven reachable commits.
- Stored refs: `main`, `origin/main`, `origin/feat-python`, `origin/HEAD`.
- Tracked files: README, `.gitattributes`, one 162-line Python TUI, six empty `.txt`
  sample files. No requirements file, package metadata, tests, license, CI, or gitignore.
- All runtime code lived in `GrepFileApp`, mixing parsing, filesystem IO, metadata,
  binary search, and UI rendering. Imports were used; no separate dead-code subsystem
  or duplicate algorithm existed.
- The README's startup path/tree was wrong after the move into `programa/`.
- Earlier C/Makefile/report placeholders were zero-byte files, already deleted by
  `22be562`. An old README described content search and linked lists without code
  implementing them. No academic PDF/report exists in the reviewed history.
- No IDE settings, caches, binaries, environment files, secrets, student identifiers,
  or hardcoded personal paths existed in tracked baseline files. Dependencies were
  undocumented beyond an unbounded `pip install textual` recommendation.

## Baseline behavior and architecture

```text
os.listdir(".") → os.path.isfile filtering → sorted filenames
               → os.stat metadata dictionary
input → startswith("grep ") → slice remainder → binary search → Rich result table
```

The application indexed immediate regular-file entries, including hidden files and
links to regular files, at startup only. Lookup compared exact names case-sensitively
and reported stored absolute path, size, and local naive modification time. It
searched **filenames only**, with no content reading, regex, recursion, or extension
restriction. The original slice accepted unquoted spaces but could not distinguish
extra arguments. That behavior is now explicit: quote filenames containing spaces.

## Findings, risks, and implemented decisions

| Finding | Risk / reason | Resolution |
| --- | --- | --- |
| Business logic inside the UI | Difficult isolated testing and reuse | Small parser, index, search, display, CLI, and app modules |
| Prefix check / string slice | Ambiguous syntax and weak diagnostics | shlex lexing, structural validation, distinct error codes |
| Nested untyped dictionaries | Fragile metadata field access | Frozen typed `Command`, `FileEntry`, `FileIndex`, and `IndexWarning` |
| Unhandled directory/stat failures | Startup crashes or stale results | Specific chained errors, visible per-entry warnings, live stat on matches |
| One-time mutable index | New files invisible indefinitely | Manual refresh, completed immutable snapshots, failed-refresh retention |
| Raw names interpreted as Rich markup | Misleading output / terminal controls | Literal `Text` rendering and visible control/format escapes |
| No package or console entry | Installation depends on launch location | pyproject, src layout, CLI entry, module entry, compatibility wrapper |
| No tests or quality tooling | Regressions unobserved | pytest core/CLI/Pilot tests, Ruff lint/format, build/install checks |
| No ignore rules | Future environment/credential commits | Python/build/IDE/credential ignores and deterministic LF text |
| Academic claims and current scope confused | Misleading portfolio story | Evidence-qualified academic docs and honest filename-only README |
| Historical personal email | Privacy exposure through commit metadata | Separate anonymization plan; no rewrite performed |
| No project license; multiple contributors | Redistribution rights unresolved | MIT recommendation documented; license left pending by owner |

No useful search behavior was removed. Original sample files and launcher path were
kept. No content-search feature, hash backend, watcher, generated parser, recursive
engine, binary bundler, mypy, or corporate contribution process was added.

## Final architecture and features

`parser.py` performs lexical/structural validation; `index.py` constructs aligned
sorted metadata snapshots; `search.py` owns binary search and current-file checks.
`app.py` handles Textual interaction; `cli.py` handles command-line arguments and
exit codes; `display.py` shares literal Rich rendering. There is no additional
service layer to inflate the design. See [architecture](docs/architecture.md).

Implemented commands: `grep <filename>`, `refresh`, `help`, `quit` in the TUI;
`mini-grep search <filename> [--directory <path>]` in the CLI. Default `mini-grep`
starts the TUI. `--help`, `--version`, `python -m mini_grep`, and the old launcher
are documented. TUI shortcuts are Ctrl+R, F1, and Ctrl+Q. Status displays directory,
index size, skipped entries, and UTC refresh time. Full scans run off the UI thread.

### Feature prioritization

| Priority | Features | Decision |
| --- | --- | --- |
| Core | Exact filenames, binary search, metadata, structural parsing | Preserve and test |
| Useful | Manual refresh, directory selection, CLI, help, quoted spaces | Implemented through shared logic |
| Future | Opt-in recursion, case/partial/glob filters, isolated content search | Defer until a concrete use case |
| Unnecessary now | GNU grep cloning, multiple backends, watchers, plugins, executable bundling | Avoid |

## Algorithms and performance

For `m` directory entries and `n` indexed files, scanning/filtering/metadata costs
O(m), sorting O(n log n), and initial indexing/full refresh O(m + n log n).
Prepared binary lookup takes O(log n), with O(1) auxiliary space. A successful
lookup additionally reads live metadata; a fresh CLI run pays indexing first.
Snapshot storage is O(m + n), including warnings, and actual bytes depend on total
name/path length. Worst-case filename comparison costs add a length factor.

Binary search remains the single backend by conscious choice: a hash set/dict would
give expected O(1) membership, but explicit sorted lookup supports the project's
academic identity. The original redundant metadata dictionary was replaced with
aligned sorted tuples. No claim of being faster than hashing or GNU grep is made.

Synthetic Windows/Python 3.11 smoke checks used 10, 100, 1,000, and 10,000 files.
10,000-file indexing took 861.668 ms; average binary lookup 2.407 µs, and lookup
with a live stat 67.805 µs. These one-run checks reveal no obvious scaling defect,
but are not scientific comparisons. [Performance details](docs/performance.md).

## Testing and verification

- **Windows / Python 3.11.9:** 77 passed, 0 failed, 0 skipped.
- **Windows / Python 3.13.5 clean environment:** 77 passed, 0 failed, 0 skipped,
  against a non-editable wheel install.
- Parser coverage: valid commands, quoting/Unicode, tabs, lowercase keyword, empty
  input, missing/extra arguments, invalid quoting, traversal, and control characters.
- Search coverage: empty/single collections, first/middle/last, absent boundaries,
  many targets, exact case, current metadata, created/deleted/replaced/inaccessible files.
- Index coverage: isolated temporary directories, empty directory, multiple extensions,
  Unicode, spaces, hidden files, metadata fields/UTC, long names, subdirectory filtering,
  links/broken links, and deterministic permission/race/root-resolution errors.
- Pilot coverage: startup and actual typed input, found/missing/invalid results,
  literal names, stale files, visible warnings, refresh/help/quit commands and shortcuts,
  failed refresh preserving the snapshot, and recovery from a missing directory.
- Ruff lint and format checks pass; standalone type checking is intentionally not
  configured. Annotations and dataclasses improve contracts without another tool.
- Editable install and console/module entry points pass in the development environment.
- Wheel/sdist build and fresh wheel install passed. Console/module searches and exit
  codes 0/1/2 were verified outside the repository with no PYTHONPATH dependence.
- The TUI also launched in a real Windows terminal, found a supplied sample, and
  exited normally. Compact help and metadata rendering preserve result space at 80×24.
- Documented demo searches, version/help commands, and the old launcher were verified.
- Linux/macOS have not run locally. CI is configured, not remotely executed.

## Dependencies, packaging, and reproducibility

Runtime: **Textual 8.2.8** and **Rich 14.3.4** tested, with minimum-tested-version
lower bounds and next-major upper bounds. Both are direct imports; Rich is explicit.
No networking or content-search dependency is used at runtime. Development tools
are pytest, Ruff, build, and pip-audit; no asynchronous pytest plugin is needed.

The virtual environment initially inherited pip 24.0 and setuptools 65.5.0.
`pip-audit --local` reported 20 advisory records (including duplicate IDs) in those
two tools. They were upgraded locally to **pip 26.2.1** and **setuptools 84.0.0**;
the build backend minimum is 83, addressing the reported fixed-version floor.
The subsequent audit reported **no known vulnerabilities** among the installed
third-party distributions. The local unpublished `mini-grep` package was explicitly
skipped by PyPI auditing; its source was reviewed separately. This is dated evidence,
not an assurance of future security or proof of no unknown vulnerabilities.

Installed metadata/license notices identify MIT for Textual/Rich and their Markdown,
linkification, and platformdirs dependencies; Pygments uses BSD-2-Clause and
typing-extensions PSF-2.0. They are installed, not vendored. No incompatible copied
source or license notices were found; authorization to license contributed project
code remains unconfirmed. [Licensing decision](docs/licensing.md).

`requirements-dev.lock` records the exact validated dependency versions without
editable paths or personal metadata. It is a pinned snapshot, not a hash/multi-OS
lock. `MANIFEST.in` packages docs, tests, samples, tooling, and the lock in the sdist;
the wheel contains application modules and distribution metadata only. Build products,
environments, and caches are ignored. Version 0.1.0 is proposed, with an Unreleased
changelog; no tag, release, or package publication exists.

## Security and privacy

All six distinct baseline blobs, seven commits, stored branches, filenames, messages,
and author/committer metadata were inspected. Regex-assisted scans covered private
contacts, paths, student identifiers, credential markers, and likely phone formats;
manual review complemented them. All baseline blobs were UTF-8 text or empty.
No secrets, private paths, matrícula/student numbers, phone/address data, PDFs, or
unnecessary document metadata were found in the reviewed tracked contents.

The historical finding is a Gmail address in the author and committer of **`22be562`**,
not in a source file. Its exact value is not republished here. Public handles and
GitHub noreply attribution remain intentional. The owner requested an anonymization
plan without execution; [privacy-history.md](docs/privacy-history.md) records the
commit, location, risk, proposed tool, backup/coordination strategy, and remote/cache
limitations. No history was rewritten and no mailmap pretending to erase it was added.

The application never executes commands, changes indexed files, reads contents, or
connects to a network. Links to external files expose metadata by design; this is
not a sandbox. TOCTOU changes remain possible after metadata checks. Absolute paths
are shown only at runtime; public captures must use sanitized paths. `.gitignore`
is preventive hygiene, not historical secret removal. See [SECURITY.md](SECURITY.md).

## Documentation and GitHub preparation

The README now describes installation, real commands, CLI exit codes, academic
lineage, current architecture, complexity, limitations, and license status. Separate
documents cover academic origin, illustrative grammar, architecture, performance,
reproducibility, licensing, history privacy, and suggested GitHub metadata.
No professor, grade, student number, personal address, or invented screenshot appears.
The original report is absent, so reconstructed productions are labeled explicitly.

CI has two jobs: Ubuntu/Python 3.11 and Windows/Python 3.13. It installs the dev extra,
runs lint/format/tests/dependency consistency, builds artifacts, and checks the version
entry point. Actions are pinned to inspected commit SHAs with read-only repository
permission and no persisted checkout credentials. The workflow is local configuration;
no remote run is claimed. [Repository description/topics](docs/github-metadata.md)
are suggestions only. No remote rename, visibility change, push, tag, or release occurred.

## Git review and remaining work

The existing history remains intact. Original authorship is preserved. New commits
use the already-configured GitHub noreply identity; no Git identity configuration
is changed. Main and stored remote refs remain at their original commits. Changes
are organized into three local commits: application refactor/packaging; tests,
benchmark, reproducibility and CI; documentation and release review. Final status,
diff, tracked-file inventory, and all-ref history are checked at handoff.

### File inventory

Added: `.gitignore`, `pyproject.toml`, `MANIFEST.in`, `requirements-dev.lock`,
`.github/workflows/ci.yml`; eight package modules under `src/mini_grep/`; five
test files under `tests/`; `scripts/benchmark.py`; `CHANGELOG.md`, `CONTRIBUTING.md`,
`SECURITY.md`, this review; and these eight documents under `docs/`:
`academic-origin.md`, `formal-language.md`, `architecture.md`, `performance.md`,
`reproducibility.md`, `privacy-history.md`, `licensing.md`, `github-metadata.md`.

Modified: `README.md`, `.gitattributes`, `programa/grep_tui.py`. Removed: **none**.
The six original empty text files remain unchanged. No local environment, cache,
temporary private mailmap, build output, or unexpected binary is tracked.

Before public/open-source publication: confirm contributor rights and add the agreed
license; review the anonymization plan and approve any later rewrite separately;
run CI after an approved push and verify Linux behavior. A real sanitized screenshot
is optional. Core implementation, tests, and documentation require no extra features.

## Publication checklist

- [x] No secrets found in inspected content/history (heuristic/manual audit scope).
- [ ] No personal identifiers: historical personal email remains intentionally.
- [x] Clean Git status at handoff; changes committed on the work branch.
- [x] Tests passing on Windows/Python 3.11 and 3.13: 77 each, 0 failed/skipped.
- [x] Lint and formatting passing.
- [x] Clean artifact installation tested outside the repository working directory.
- [x] README accurately distinguishes academic origin and current implementation.
- [ ] License present: intentionally pending contributor authorization.
- [x] CI configured; remote execution pending an authorized push.
- [x] No unwanted binaries/environments/caches selected for tracking.
- [x] No private local paths in authored public-facing files.
- [x] Complete locally available baseline history reviewed; anonymization not executed.
- [x] Documented entry points and README examples verified; illustrative absent names labeled.

## Recommendation

The technical refactor is complete and locally verified. Publication preparation
has three explicit warnings: contributor authorization/license selection is pending;
the historical personal email remains until a separately approved operation; and
CI/Linux execution still needs remote evidence. The owner chose to defer licensing
and requested only an anonymization plan. Those are recorded decisions, not unfinished
implementation. Obtain publication approval and resolve the desired licensing/privacy
policy before changing remote state. No publication is authorized by this task.

**READY WITH WARNINGS**
