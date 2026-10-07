"""Build immutable, non-recursive directory snapshots using pathlib."""

import stat
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


class FileIndexError(OSError):
    """The directory could not be read; a partial index must not replace the old one."""


@dataclass(frozen=True)
class FileEntry:
    name: str
    path: Path
    size: int
    modified_at: datetime


@dataclass(frozen=True)
class IndexWarning:
    path: Path
    reason: str


@dataclass(frozen=True)
class FileIndex:
    """Aligned entries and names, sorted by Python's case-sensitive string ordering."""

    directory: Path
    entries: tuple[FileEntry, ...]
    names: tuple[str, ...]
    refreshed_at: datetime
    warnings: tuple[IndexWarning, ...] = ()


def read_entry(path: Path) -> FileEntry | None:
    """Read metadata once; follow links to regular files, preserving the original behavior."""
    metadata = path.stat()
    if not stat.S_ISREG(metadata.st_mode):
        return None
    return FileEntry(
        name=path.name,
        path=path,
        size=metadata.st_size,
        modified_at=datetime.fromtimestamp(metadata.st_mtime, tz=UTC),
    )


def build_index(directory: Path) -> FileIndex:
    """Scan immediate children, report unreadable entries, and sort only once.

    Directory-level failures raise FileIndexError with the OS error chained.
    Per-entry failures become visible warnings, including files removed during scanning.
    """
    entries: list[FileEntry] = []
    warnings: list[IndexWarning] = []
    try:
        root = directory.resolve(strict=True)
        for path in root.iterdir():
            try:
                entry = read_entry(path)
            except (OSError, ValueError, OverflowError) as error:
                warnings.append(IndexWarning(path, str(error)))
                continue
            if entry is not None:
                entries.append(entry)
    except (OSError, ValueError, RuntimeError) as error:
        raise FileIndexError(f"Cannot index directory '{directory}': {error}") from error

    entries.sort(key=lambda entry: entry.name)
    return FileIndex(
        directory=root,
        entries=tuple(entries),
        names=tuple(entry.name for entry in entries),
        refreshed_at=datetime.now(UTC),
        warnings=tuple(warnings),
    )
