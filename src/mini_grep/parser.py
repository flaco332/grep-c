"""Parse a small command language without executing shell commands."""

import shlex
import unicodedata
from dataclasses import dataclass
from typing import Literal

CommandName = Literal["grep", "refresh", "help", "quit"]


class CommandSyntaxError(ValueError):
    """A user command does not belong to the supported command language."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Command:
    name: CommandName
    filename: str | None = None


def validate_filename(filename: str) -> None:
    """Accept a basename, including spaces and Unicode, but never a path or control text."""
    if (
        not filename
        or filename in {".", ".."}
        or "/" in filename
        or "\\" in filename
        or any(unicodedata.category(char) == "Cc" for char in filename)
    ):
        raise CommandSyntaxError(
            "invalid_filename",
            "Use a filename without path separators or control characters. "
            'Quote names with spaces: grep "annual report.txt"',
        )


def parse_command(source: str) -> Command:
    """Lex with shlex, then validate the keyword, arity, and filename separately."""
    if not source.strip():
        raise CommandSyntaxError("empty_command", "Empty command. Use: grep <filename> or help.")
    # Checking the source prevents shlex whitespace rules from hiding control characters.
    if any(unicodedata.category(char) == "Cc" and char != "\t" for char in source):
        raise CommandSyntaxError("invalid_syntax", "Commands must fit on one line.")
    try:
        tokens = shlex.split(source, comments=False, posix=True)
    except ValueError as error:
        raise CommandSyntaxError("invalid_syntax", "Invalid quoting. Close all quotes.") from error

    keyword = tokens[0]
    if keyword not in {"grep", "refresh", "help", "quit"}:
        raise CommandSyntaxError(
            "unknown_command", "Unknown command. Use grep, refresh, help, or quit."
        )
    expected = 2 if keyword == "grep" else 1
    if len(tokens) < expected:
        raise CommandSyntaxError("missing_argument", "Missing filename. Use: grep <filename>.")
    if len(tokens) > expected:
        raise CommandSyntaxError(
            "too_many_arguments",
            'Too many arguments. Quote filenames with spaces: grep "my file.txt".',
        )
    if keyword == "grep":
        validate_filename(tokens[1])
        return Command("grep", tokens[1])
    if keyword == "refresh":
        return Command("refresh")
    if keyword == "help":
        return Command("help")
    return Command("quit")
