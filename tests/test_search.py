from pathlib import Path

import pytest

from mini_grep.index import build_index
from mini_grep.parser import CommandSyntaxError
from mini_grep.search import FileAccessError, binary_search, find_file


@pytest.mark.parametrize(
    ("names", "target", "position"),
    [
        ([], "a", -1),
        (["a"], "a", 0),
        (["a"], "b", -1),
        (["a", "b", "c", "d", "e"], "a", 0),
        (["a", "b", "c", "d", "e"], "c", 2),
        (["a", "b", "c", "d", "e"], "e", 4),
        (["a", "b", "c", "d", "e"], "0", -1),
        (["a", "b", "c", "d", "e"], "z", -1),
        (["a", "c"], "b", -1),
        (["A", "a"], "A", 0),
    ],
)
def test_binary_search_boundaries(names, target, position):
    assert binary_search(names, target) == position


def test_binary_search_matches_membership_over_many_targets():
    names = [f"file-{number:04}.txt" for number in range(0, 1000, 2)]
    for number in range(1000):
        target = f"file-{number:04}.txt"
        expected = number // 2 if number % 2 == 0 else -1
        assert binary_search(names, target) == expected


def test_snapshot_refresh_and_fresh_metadata(tmp_path):
    path = tmp_path / "report.txt"
    path.write_text("old", encoding="utf-8")
    index = build_index(tmp_path)
    assert find_file(index, "report.txt").size == 3
    assert find_file(index, "missing") is None
    assert find_file(index, "REPORT.TXT") is None
    path.write_text("longer content", encoding="utf-8")
    assert find_file(index, "report.txt").size == len("longer content")
    (tmp_path / "new.txt").touch()
    assert find_file(index, "new.txt") is None
    assert find_file(build_index(tmp_path), "new.txt") is not None


def test_deleted_file_reports_stale_index(tmp_path):
    path = tmp_path / "gone.txt"
    path.touch()
    index = build_index(tmp_path)
    path.unlink()
    with pytest.raises(FileAccessError, match="Refresh") as caught:
        find_file(index, "gone.txt")
    assert isinstance(caught.value.__cause__, FileNotFoundError)
    assert find_file(build_index(tmp_path), "gone.txt") is None


def test_file_replaced_by_directory(tmp_path):
    path = tmp_path / "changed.txt"
    path.touch()
    index = build_index(tmp_path)
    path.unlink()
    path.mkdir()
    with pytest.raises(FileAccessError, match="regular file"):
        find_file(index, "changed.txt")


def test_access_denied_during_search(tmp_path, monkeypatch):
    (tmp_path / "locked.txt").touch()
    index = build_index(tmp_path)

    def deny_stat(self, **kwargs):
        raise PermissionError("access denied")

    monkeypatch.setattr(Path, "stat", deny_stat)
    with pytest.raises(FileAccessError) as caught:
        find_file(index, "locked.txt")
    assert isinstance(caught.value.__cause__, PermissionError)


def test_search_cannot_escape_directory(tmp_path):
    with pytest.raises(CommandSyntaxError):
        find_file(build_index(tmp_path), "../outside.txt")
