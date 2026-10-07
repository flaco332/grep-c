# Security

Mini Grep reads directory entries and filesystem metadata. It does not read file
contents, execute input commands, modify searched files, or use the network at
runtime. It follows symlinks to regular files, which may expose target metadata
outside the indexed directory. It is not a filesystem sandbox.

Untrusted filenames and errors are rendered as literal text; control characters
are displayed visibly. Avoid sharing terminal captures containing personal paths
or files. Do not add secrets as test data, even in temporary commits.

For dependency checks, install the dev extra and run `python -m pip_audit --local`
with network access. A successful audit only addresses known advisories for the
installed versions at that time. The unpublished local package cannot be audited
against PyPI; its code is reviewed separately.

Report security-sensitive details through a private channel with the maintainer;
use GitHub's private vulnerability reporting if the maintainer enables it. Do not
put exploit secrets or personal data into public issues. No security-reporting
endpoint or support SLA is currently configured. Historical email handling is
documented in [privacy review](docs/privacy-history.md).
