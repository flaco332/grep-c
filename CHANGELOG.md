# Changelog

## Unreleased — proposed 0.1.0

No version has been tagged or published. The older academic commits remain in Git;
this changelog starts with the first packaging effort rather than inventing releases.

### Added

- Installable `mini-grep` command and `python -m mini_grep` entry point.
- Exact filename CLI, directory selection, and consistent exit codes.
- Explicit command parser with quoted filenames and distinct syntax errors.
- Manual refresh, help, quit, status, and keyboard shortcuts in the Textual TUI.
- Typed immutable snapshots, UTC metadata, per-entry warnings, and stale-file errors.
- Isolated parser, index, search, CLI, and headless TUI tests; smoke benchmark.
- Ruff, packaging, GitHub Actions, and academic/architecture/privacy documentation.

### Changed

- Moved application logic from `programa/grep_tui.py` into `src/mini_grep/`; kept
  that path as an installed-package compatibility launcher and kept its sample files.
- Replaced ad hoc path operations and nested dictionaries with pathlib and dataclasses.
- Kept case-sensitive binary search; matches re-read live metadata before display.
- Clarified filename-only scope and the difference from the original formal language.
- Set the maintained Python baseline to 3.11, matching the tested environments.

### Pending

- Contributor authorization and license selection.
- Separate approved history anonymization if desired; no rewriting performed.
