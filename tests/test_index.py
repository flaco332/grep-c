from datetime import UTC, datetime
from pathlib import Path

import pytest

from mini_grep.index import FileIndexError, build_index


def test_index_filters_directories_and_collects_metadata(tmp_path):
    names = ["z.txt", "a.py", ".hidden", "canción.txt", "space name.md", "README"]
    for name in names:
        (tmp_path / name).write_bytes(b"sample")
    nested = tmp_path / "subdirectory"
    nested.mkdir()
    (nested / "nested.txt").touch()
    before = datetime.now(UTC)
    index = build_index(tmp_path)
    assert index.directory == tmp_path.resolve()
    assert index.names == tuple(sorted(names))
    assert tuple(entry.name for entry in index.entries) == index.names
    assert not index.warnings
    assert index.refreshed_at >= before
    for entry in index.entries:
        assert entry.path == tmp_path.resolve() / entry.name
        assert entry.size == 6
        assert entry.modified_at == datetime.fromtimestamp(entry.path.stat().st_mtime, UTC)


def test_empty_directory(tmp_path):
    index = build_index(tmp_path)
    assert index.names == index.entries == index.warnings == ()


def test_directory_and_filename_with_spaces_and_long_name(tmp_path):
    directory = tmp_path / "directory with spaces"
    directory.mkdir()
    name = "a" * 100 + ".txt"
    (directory / name).touch()
    index = build_index(directory)
    assert index.names == (name,)
    assert index.entries[0].path.parent == directory


@pytest.mark.parametrize("kind", ["missing", "file"])
def test_invalid_directory(tmp_path, kind):
    directory = tmp_path / "invalid"
    if kind == "file":
        directory.touch()
    with pytest.raises(FileIndexError) as caught:
        build_index(directory)
    assert isinstance(caught.value.__cause__, OSError)


def test_directory_permission_failure_keeps_os_cause(tmp_path, monkeypatch):
    def deny_iteration(self):
        raise PermissionError("access denied")

    monkeypatch.setattr(Path, "iterdir", deny_iteration)
    with pytest.raises(FileIndexError) as caught:
        build_index(tmp_path)
    assert isinstance(caught.value.__cause__, PermissionError)


def test_unresolvable_root_reports_index_error(tmp_path, monkeypatch):
    def looped_path(self, strict=False):
        raise RuntimeError("symlink loop")

    monkeypatch.setattr(Path, "resolve", looped_path)
    with pytest.raises(FileIndexError, match="symlink loop") as caught:
        build_index(tmp_path)
    assert isinstance(caught.value.__cause__, RuntimeError)


@pytest.mark.parametrize("failure", [PermissionError("denied"), FileNotFoundError("removed")])
def test_per_entry_failures_are_visible(tmp_path, monkeypatch, failure):
    (tmp_path / "good.txt").touch()
    (tmp_path / "bad.txt").touch()
    original = Path.stat

    def interrupted_stat(self, **kwargs):
        if self.name == "bad.txt":
            raise failure
        return original(self, **kwargs)

    monkeypatch.setattr(Path, "stat", interrupted_stat)
    index = build_index(tmp_path)
    assert index.names == ("good.txt",)
    assert len(index.warnings) == 1
    assert index.warnings[0].path.name == "bad.txt"
    assert index.warnings[0].reason == str(failure)


def test_symlinks_follow_regular_targets_and_warn_on_broken_links(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("data", encoding="utf-8")
    try:
        (tmp_path / "link.txt").symlink_to(target)
        (tmp_path / "broken.txt").symlink_to(tmp_path / "missing.txt")
        (tmp_path / "directory-link").symlink_to(tmp_path, target_is_directory=True)
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"This environment cannot create symlinks: {error}")
    index = build_index(tmp_path)
    assert index.names == ("link.txt", "target.txt")
    assert index.entries[0].path.name == "link.txt"
    assert index.entries[0].size == 4
    assert len(index.warnings) == 1
    assert index.warnings[0].path.name == "broken.txt"
