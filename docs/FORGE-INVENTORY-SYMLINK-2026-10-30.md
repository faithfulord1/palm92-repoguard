# Inventory scope repair, 30 October 2026

Reproduced two failures: replacing a tracked file's parent directory with a
symlink caused the inventory to read an outside-checkout file or an untracked
internal file. Checking only the final filename did not enforce the documented
symlink exclusion.

The scanner now checks every lexical path component for a symlink before file
metadata or content reads. Two fictional regression fixtures cover external and
internal parent-directory symlinks. No private data or real external service is
used. The scanner remains read-only.

Limit: this is a static-checkout guard, not race-proof filesystem isolation.
Do not scan a checkout being concurrently modified by an untrusted process.

Plan A: review and run the existing Python CI matrix before merge. Plan B: run
the same pytest suite locally without hosting or model dependencies.
