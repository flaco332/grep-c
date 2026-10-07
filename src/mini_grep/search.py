"""Exact filename lookup using the project's educational binary search algorithm."""

from collections.abc import Sequence

from mini_grep.index import FileEntry, FileIndex, read_entry
from mini_grep.parser import validate_filename


class FileAccessError(OSError):
    """An indexed filename became inaccessible or stopped being a regular file."""


def binary_search(names: Sequence[str], target: str) -> int:
    """Return the position or -1; names must already be sorted in ascending order.

    A hash table would give average O(1) membership; we retain O(log n) binary
    search to make the sorted-index invariant and academic algorithm inspectable.
    """
    low, high = 0, len(names) - 1
    while low <= high:
        middle = (low + high) // 2
        value = names[middle]
        if value == target:
            return middle
        if value < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def find_file(index: FileIndex, filename: str) -> FileEntry | None:
    """Search the snapshot, then check current metadata before reporting FOUND.

    Newly created names need refresh. No metadata check can guarantee the file
    stays present after returning; this application never opens file contents.
    """
    validate_filename(filename)
    position = binary_search(index.names, filename)
    if position == -1:
        return None
    path = index.entries[position].path
    try:
        entry = read_entry(path)
    except (OSError, ValueError, OverflowError) as error:
        raise FileAccessError(
            f"Cannot access indexed file '{filename}': {error}. Refresh the index."
        ) from error
    if entry is None:
        raise FileAccessError(f"'{filename}' is no longer a regular file. Refresh the index.")
    return entry
