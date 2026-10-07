# Suggested GitHub metadata

These are proposals only. No remote metadata, visibility, tags, release, or GitHub
settings were changed.

- **Repository name:** `mini-grep`. The current local/remote name `grep-c` is retained.
- **Description:** `Academic filename search in Python with binary search, a Textual TUI, and a tested lexer/parser architecture.`
- **Topics:** `python`, `textual`, `rich`, `binary-search`, `algorithms`, `terminal-ui`,
  `parser`, `formal-languages`, `theory-of-computation`, `educational-project`.

The formal-language topics describe the documented academic lineage. Avoid implying
an implemented automata engine or generated lexer. No speed, security, or production
readiness badges are justified. CI is configured but has not run on GitHub because
this branch has not been pushed.

## Recommended version

Package metadata uses **0.1.0**, the proposed first packaged version. It is a
pre-1.0 release with a deliberately small interface. `CHANGELOG.md` remains
**Unreleased**; no tag or release date was invented. Use Semantic Versioning for
future releases, documenting interface changes while the project remains pre-1.0.

## Optional screenshot

Capture a real 80×24 or larger terminal running `mini-grep` against a sanitized demo
directory. Show a found result, the command input, status, and shortcuts. Use neutral
paths with no home-directory username or personal files; inspect the whole image
before committing it. Place an approved capture in `docs/assets/` and link it from
the README. No placeholder image or fabricated screenshot is included.
