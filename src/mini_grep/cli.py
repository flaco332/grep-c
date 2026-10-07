"""Launch the TUI or run a single filename search with useful exit codes."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console

from mini_grep import __version__
from mini_grep.display import file_table, literal
from mini_grep.index import FileIndexError, build_index
from mini_grep.parser import CommandSyntaxError, validate_filename
from mini_grep.search import FileAccessError, find_file


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exact filename search; never searches file contents."
    )
    parser.add_argument("--version", action="version", version=f"Mini Grep {__version__}")
    parser.add_argument(
        "-d", "--directory", type=Path, default=Path("."), help="directory to index"
    )
    subcommands = parser.add_subparsers(dest="command")
    search = subcommands.add_parser("search", help="search one filename without starting the TUI")
    search.add_argument("filename", help="exact filename; quote names with spaces")
    search.add_argument("-d", "--directory", type=Path, default=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.command is None:
        # The core modules and CLI tests do not need to initialize Textual.
        from mini_grep.app import GrepFileApp

        GrepFileApp(args.directory).run()
        return 0

    console = Console()
    errors = Console(file=sys.stderr)
    try:
        validate_filename(args.filename)
        index = build_index(args.directory)
        for warning in index.warnings:
            errors.print(literal(f"WARNING: {warning.path.name}: {warning.reason}"))
        entry = find_file(index, args.filename)
    except (CommandSyntaxError, FileIndexError, FileAccessError) as error:
        errors.print(literal(f"ERROR: {error}"), style="bold red")
        return 2
    if entry is None:
        console.print(literal(f"NOT FOUND: {args.filename}"), style="yellow")
        return 1
    console.print(file_table(entry))
    return 0
