# Licensing status

**License pending.** The repository owner explicitly requested leaving the license
undecided until contributor authorization is established. No `LICENSE` or SPDX
license declaration has been added. Public visibility alone does not grant an
open-source license.

MIT is the recommended eventual license for this small educational portfolio
project. The locally available history contains a Python contribution by another
author. Preserve that attribution and obtain authorization from all relevant rights
holders before licensing their work. An empty historical C scaffold contributes no
implemented search logic; the original academic report is unavailable for inspection.

Inspection found no copied third-party source trees, bundled libraries, or existing
license notices to remove. This does not establish the provenance of every historical
line. Textual and Rich are installed as dependencies, not vendored; their installed
package metadata and license files identify MIT licensing. Runtime transitive packages
also retain their own license notices in their distributions. See the dependency
review in `PUBLIC_RELEASE_REVIEW.md` for the exact versions inspected.

Before choosing MIT:

1. Confirm the rights to distribute the academic code and its contributors' work.
2. Add the MIT text with an agreed copyright attribution.
3. Add an SPDX `MIT` declaration to `pyproject.toml` and include `LICENSE` in the sdist.
4. Replace the pending status in the README and release review.

GitHub's [licensing guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
explains the effect of leaving a repository without a license. This is a
release-preparation decision, not a license grant or a legal opinion.
