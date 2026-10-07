"""Shared, literal terminal rendering for the CLI and TUI."""

import unicodedata

from rich.table import Table
from rich.text import Text

from mini_grep.index import FileEntry

HELP = (
    "Exact filename search; case-sensitive, immediate directory only.\n"
    'grep <filename>       Search a name (spaces: grep "my file.txt")\n'
    "refresh               Rebuild the directory index\n"
    "help                  Show this help\n"
    "quit                  Exit\n"
    "Ctrl+R refresh | F1 help | Ctrl+Q quit"
)


def literal(value: str) -> Text:
    """Disable markup and expose control/format characters from filesystem names."""
    safe = "".join(
        char if unicodedata.category(char) not in {"Cc", "Cf", "Cs"} else ascii(char)[1:-1]
        for char in value
    )
    return Text(safe)


def file_table(entry: FileEntry) -> Table:
    table = Table(title="FOUND", title_style="bold green", expand=True, show_header=False, box=None)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", overflow="fold")
    table.add_row("Name", literal(entry.name))
    table.add_row("Path", literal(str(entry.path)))
    table.add_row("Size (bytes)", str(entry.size))
    table.add_row("Modified (UTC)", entry.modified_at.strftime("%Y-%m-%d %H:%M:%S"))
    return table
