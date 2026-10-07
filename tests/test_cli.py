import os
import subprocess
import sys

import pytest

from mini_grep.cli import main
from mini_grep.display import literal
from mini_grep.index import FileIndexError


@pytest.mark.parametrize("option_order", ["before", "after"])
def test_cli_found_and_quoted_filename(tmp_path, capsys, option_order):
    (tmp_path / "space name.txt").write_bytes(b"abc")
    directory = ["--directory", str(tmp_path)]
    search = ["search", "space name.txt"]
    argv = directory + search if option_order == "before" else search + directory
    assert main(argv) == 0
    output = capsys.readouterr()
    assert "FOUND" in output.out
    assert "space name.txt" in output.out
    assert "Size (bytes)" in output.out
    assert not output.err


def test_cli_not_found(tmp_path, capsys):
    assert main(["search", "missing.txt", "--directory", str(tmp_path)]) == 1
    assert "NOT FOUND" in capsys.readouterr().out


@pytest.mark.parametrize("filename", ["../outside.txt", ""])
def test_cli_invalid_filename(tmp_path, capsys, filename):
    assert main(["search", filename, "--directory", str(tmp_path)]) == 2
    assert "ERROR" in capsys.readouterr().err


def test_cli_directory_error(tmp_path, capsys):
    assert main(["search", "x", "--directory", str(tmp_path / "missing")]) == 2
    assert "Cannot index directory" in capsys.readouterr().err


def test_cli_preserves_actionable_os_errors(monkeypatch, capsys):
    def deny_index(directory):
        raise FileIndexError("access denied")

    monkeypatch.setattr("mini_grep.cli.build_index", deny_index)
    assert main(["search", "file.txt"]) == 2
    assert "access denied" in capsys.readouterr().err


def test_module_entry_point_outside_repository(tmp_path):
    (tmp_path / "demo.txt").touch()
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, "-m", "mini_grep", "search", "demo.txt"],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "FOUND" in result.stdout


def test_untrusted_text_is_literal_and_controls_are_visible():
    rendered = literal("[red]name.txt\x1b[2J\u202e")
    assert "[red]name.txt" in rendered.plain
    assert "\x1b" not in rendered.plain
    assert "\u202e" not in rendered.plain
    assert "\\x1b" in rendered.plain
    assert "\\u202e" in rendered.plain
    assert not rendered.spans
