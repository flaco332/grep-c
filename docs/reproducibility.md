# Installation and reproducibility

The package uses `pyproject.toml`, a `src/` layout, and a console script. Runtime
dependencies are Textual and Rich. Rich is explicit because both user interfaces
import it directly rather than relying on Textual's transitive dependency forever.

## Normal install

Create and activate a virtual environment as shown in the README, then run
`python -m pip install -e .`. Run `mini-grep` or `python -m mini_grep` from any
working directory. Use `--directory programa` from the repository root to inspect
the provided samples. The wrapper `python programa/grep_tui.py` also needs the
installed package; no source-path manipulation or duplicate implementation exists.

## Repeat the validated development environment

`requirements-dev.lock` is a version-pinned snapshot of installed runtime and
development dependencies, excluding the local package and all personal paths.
It includes tooling packages only to reproduce checks; they are not application
runtime dependencies. It is not a hashed, multi-platform resolver lock.

In a fresh virtual environment:

```bash
python -m pip install -r requirements-dev.lock
python -m pip install --no-build-isolation -e ".[dev]"
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m pip check
```

The snapshot includes a patched setuptools build backend. `--no-build-isolation`
here uses that installed backend, rather than resolving a new one. Normal isolated
builds use the lower bound declared in `pyproject.toml`. Dependency updates should
regenerate and audit the snapshot deliberately; available wheels and advisory data
can change, so reproducibility is not a perpetual security guarantee.

## Build and install artifacts

```bash
python -m build
```

This creates an sdist and a wheel in ignored `dist/`. `MANIFEST.in` includes docs,
tests, original samples, and the benchmark in the sdist; the wheel contains only
the package and standard distribution metadata. Neither artifact is committed.
Install the resulting wheel in a fresh environment with `python -m pip install
<wheel-path>`. Test its console script and `python -m mini_grep` outside the
repository working directory to detect accidental dependence on the checkout.

## Platform evidence

Local verification targets Windows with Python 3.11.9 and 3.13.5. Headless Pilot
tests exercise startup, input, results, refresh, errors, and exit. Terminal styling
and keyboard behavior still depend on the user's terminal emulator.

The GitHub Actions workflow targets Ubuntu/Python 3.11 and Windows/Python 3.13,
with execution recorded in the release review. Linux and macOS were not run locally;
portability on untested platforms remains an implementation goal. The same-repository
task uses fresh virtual environments instead of a second cloned project.
