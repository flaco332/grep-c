# Performance smoke check

Measured locally on Windows / CPython 3.11.9, 2026-10-06, using
`python scripts/benchmark.py`. Each directory contains newly generated empty files
in a temporary location. File creation is excluded from the index timing; 1,000
repeated lookups of the last sorted name produce mean lookup timings.

| Files | Index (ms) | Binary lookup (µs) | Lookup + live stat (µs) |
| ---: | ---: | ---: | ---: |
| 10 | 1.152 | 0.557 | 115.555 |
| 100 | 11.538 | 1.406 | 103.148 |
| 1,000 | 99.168 | 1.921 | 78.682 |
| 10,000 | 861.668 | 2.407 | 67.805 |

These are one-run sanity checks, not statistically controlled benchmarks or a
comparison against GNU grep or hashing. Caches, antivirus, storage, filename length,
OS scheduling, and repeated-access warming affect the results; the decreasing stat
timings do not mean filesystem access becomes faster as the index grows.

The smoke check verifies correct indexing and lookup at each size. No obvious
scaling defect appeared. Metadata system calls dominate the matched-file cost here;
binary search alone requires very little time. Large or remote directories may be
much slower. The TUI runs full scans in a background thread to keep interaction
available while indexing; it does not cache filesystem changes automatically.

Complexity remains O(m + n log n) per index/refresh and O(log n) lookup after sorting,
subject to string-comparison and filesystem costs. No performance claim relies
solely on these timings. Use the script to reproduce the check on another platform.
