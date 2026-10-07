"""Small filesystem smoke benchmark, not a scientific performance claim.

Run from an installed checkout: python scripts/benchmark.py
All generated files live in a TemporaryDirectory and are removed on exit.
"""

import argparse
import tempfile
from pathlib import Path
from time import perf_counter

from mini_grep.index import build_index
from mini_grep.search import binary_search, find_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counts", type=int, nargs="+", default=[10, 100, 1000, 10000])
    args = parser.parse_args()
    if any(count <= 0 for count in args.counts):
        parser.error("counts must be positive")
    print("files,index_ms,lookup_us,lookup_with_stat_us")
    for count in args.counts:
        with tempfile.TemporaryDirectory(prefix="mini-grep-benchmark-") as temporary:
            directory = Path(temporary)
            for number in range(count):
                (directory / f"file-{number:05}.txt").touch()
            start = perf_counter()
            index = build_index(directory)
            index_ms = (perf_counter() - start) * 1000
            assert len(index.entries) == count
            target = index.names[-1]
            repetitions = 1000
            start = perf_counter()
            for _ in range(repetitions):
                assert binary_search(index.names, target) == count - 1
            lookup_us = (perf_counter() - start) * 1_000_000 / repetitions
            start = perf_counter()
            for _ in range(repetitions):
                assert find_file(index, target) is not None
            with_stat_us = (perf_counter() - start) * 1_000_000 / repetitions
            print(f"{count},{index_ms:.3f},{lookup_us:.3f},{with_stat_us:.3f}")


if __name__ == "__main__":
    main()
