"""Compatibility launcher for the original academic demo directory.

Install the package from the repository root first: python -m pip install -e .
The process working directory still determines which files are indexed.
"""

from mini_grep.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
