import pytest

from mini_grep.parser import Command, CommandSyntaxError, parse_command, validate_filename


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("grep file.txt", Command("grep", "file.txt")),
        ("  grep\tfile.txt  ", Command("grep", "file.txt")),
        ('grep "annual report.txt"', Command("grep", "annual report.txt")),
        ("grep 'canción.txt'", Command("grep", "canción.txt")),
        ("grep .hidden", Command("grep", ".hidden")),
        ("grep README", Command("grep", "README")),
        ("grep #notes.md", Command("grep", "#notes.md")),
        ('grep " leading space.txt"', Command("grep", " leading space.txt")),
        ("help", Command("help")),
        ("refresh", Command("refresh")),
        ("quit", Command("quit")),
    ],
)
def test_valid_commands(source, expected):
    assert parse_command(source) == expected


@pytest.mark.parametrize(
    ("source", "code"),
    [
        ("", "empty_command"),
        ("  ", "empty_command"),
        ("grep", "missing_argument"),
        ("grep ", "missing_argument"),
        ("something file.txt", "unknown_command"),
        ("GREP file.txt", "unknown_command"),
        ("grep file.txt extra", "too_many_arguments"),
        ("refresh extra", "too_many_arguments"),
        ('grep "unfinished', "invalid_syntax"),
        ('grep ""', "invalid_filename"),
        ("grep ../file.txt", "invalid_filename"),
        ("grep /file.txt", "invalid_filename"),
        ('grep "C:\\file.txt"', "invalid_filename"),
        ("grep .", "invalid_filename"),
        ("grep ..", "invalid_filename"),
        ("grep file.txt\nquit", "invalid_syntax"),
        ("grep \x1b[31m.txt", "invalid_syntax"),
        ('grep "tab\tname.txt"', "invalid_filename"),
    ],
)
def test_invalid_commands_have_distinct_codes(source, code):
    with pytest.raises(CommandSyntaxError) as caught:
        parse_command(source)
    assert caught.value.code == code
    assert str(caught.value)


@pytest.mark.parametrize("filename", ["", ".", "..", "a/b", "a\\b", "a\x00b", "a\x85b"])
def test_filename_validation_reused_by_cli_and_search(filename):
    with pytest.raises(CommandSyntaxError):
        validate_filename(filename)
