# Contributing

Keep Mini Grep small and educational. Preserve exact filename search and the
documented binary-search invariant; discuss content search or new backends before
expanding the scope. Licensing is pending: see [licensing](docs/licensing.md).

From the repository root, use Python 3.11 or newer in a virtual environment:

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python -m build
```

For formatting changes, run `python -m ruff format .`. For dependency updates,
run `python -m pip check` and `python -m pip_audit --local`; review the resolved
versions before updating `requirements-dev.lock`. The lock is a validated dependency
snapshot, not a cross-platform hash lock or a guarantee of future vulnerability status.

Tests should use temporary directories, not personal files. Permission failures are
simulated deterministically; symlink tests may skip where creation is unavailable.
Use Textual's headless Pilot for a few behavioral UI checks, without brittle pixel
snapshots. No standalone type checker is configured; keep precise annotations and
check public behavior with tests.

Work on a branch and make small, descriptive commits. Include the reason for the
change and relevant test results in a pull request. Do not commit environments,
build artifacts, credentials, personal contacts, or academic identifiers. Update
the README when behavior changes and put unpublished changes under `Unreleased`.
