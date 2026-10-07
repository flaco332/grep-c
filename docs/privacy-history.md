# Privacy review and proposed anonymization

## Finding

The complete locally available history initially contained seven commits and six
distinct file-content blobs. All branches, commit messages, author/committer metadata,
historical filenames, and blobs were reviewed; `git fsck --full` found no dangling
objects. No PDFs, office documents, student IDs, credentials, personal paths, or
binary blobs were present. Remote GitHub account data and objects absent from this
clone are outside this audit.

Commit `22be5620797ee154996065265c2cb812dd4f3614` has a **personal Gmail address**
in both author and committer metadata for the handle `WhosAnder`. The address is
intentionally not repeated in public-facing documentation. Locate it privately with:

```bash
git show --no-patch --format=fuller 22be562
```

This is commit metadata, not a source-file secret. Deleting a file or adding
`.gitignore` cannot remove it. It is reachable through both `main` and the stored
`origin/feat-python` branch. Exposure can enable contact scraping or identity
correlation; no credential rotation is indicated by this finding.

Other authors use GitHub noreply addresses. Their public account handles remain
intentional attribution. University, course name, technologies, and academic context
can remain. Student IDs, private contact details, system usernames, personal absolute
paths, and credentials should not enter tracked files or screenshots.

## Owner decision

The owner requested an anonymization plan **without execution**, then authorized
public GitHub publication. Existing commits and authorship remain unchanged; no
force push or history rewrite is performed. Publication consequently exposes the
historical contact metadata described above. The release checklist does not claim
that all personal identifiers have been removed. The plan below remains a separate
future operation requiring its own authorization.

## Plan for a later authorized operation

1. Coordinate with the affected contributor and agree on a verified GitHub noreply
   address or a neutral identity, preserving authorship credit.
2. Stop concurrent development and record every branch/tag tip. Make a verified
   backup before rewriting; arrange it as a separate maintenance operation, not as
   part of this same-directory refactor.
3. Prepare a **private**, untracked mailmap with the exact old address and approved
   replacement. Do not copy the old address into a public issue or document.
4. Use `git filter-repo --mailmap <private-mailmap-file>` in the controlled maintenance
   checkout, covering all relevant refs. This is a future command outline, not an
   instruction to run it now. Follow the tool's fresh-clone protection rather than
   bypassing it with `--force` in the working repository.
5. Inspect author and committer fields, all refs, and blob contents again. Verify
   that the personal address is absent from raw objects, not just `git log`'s display.
6. Compare resulting file trees, run the tests, and inspect remotes: filter-repo may
   remove the origin remote to prevent accidental pushes. Every rewritten descendant
   changes identity; commit signatures and old links may no longer validate.
7. Obtain separate approval before updating the remote. Coordinate collaborator
   reclones and handle old branches, pull-request references, forks, and caches.
   Rewriting this local clone cannot erase copies already held elsewhere.

A committed `.mailmap` only changes presentation in supporting tools. It does not
erase original author metadata and can itself disclose the old address. It is not
sufficient privacy remediation here. See the primary
[git-filter-repo documentation](https://github.com/newren/git-filter-repo) before the
future operation; no rewriting tool was installed or run during this preparation.
