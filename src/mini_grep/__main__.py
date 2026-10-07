"""Support ``python -m mini_grep`` using the same entry point as the CLI."""

from mini_grep.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
