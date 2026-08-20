# M3 Incremental Update Report

Status: **passed**

The simulation rebuilds an isolated Markdown fixture through the same public `build_corpus` seam. Chunk IDs stay stable for content changes within the same path/heading identity; normalized-content hashes identify modifications.

| Operation | Unchanged | Added | Modified | Deleted | Pass |
| --- | ---: | ---: | ---: | ---: | --- |
| Modify | 0 | 0 | 1 | 0 | True |
| Add | 1 | 1 | 0 | 0 | True |
| Delete | 1 | 0 | 0 | 1 | True |

This seam is ready for M4 to skip unchanged IDs/hashes and distinguish additions, modifications, and deletions without performing any embedding call in M3.
