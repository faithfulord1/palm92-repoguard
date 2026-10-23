# FORGE evidence: non-UTF-8 inventory resilience

Date: 2026-10-23

## Verified problem

Git permits tracked path bytes that are not valid UTF-8. RepoGuard's PHP inventory decoded the null-delimited `git ls-files` result with strict UTF-8. A repository containing one such filename caused `UnicodeDecodeError`, preventing the scanner from returning any evidence.

The regression test first reproduced that failure with a tracked `legacy-\\xff.php` fixture.

## Change

The inventory now decodes Git path output with the operating system's filesystem decoder and its surrogate-escape behavior. This preserves a reversible representation of unusual path bytes while keeping the scan read-only.

The regression test confirms that:

- the evidence run completes;
- the PHP indicator is retained; and
- encoding the reported path with `os.fsencode` produces the original Git path bytes.

CI now runs the full dependency-minimal suite on Python 3.11, 3.12 and 3.13 with read-only repository permissions.

## Scope and limit

This change protects inventory availability from malformed or legacy Git filename encoding. It does not inspect untracked files, dependencies, hosting, deployed PHP versions or third-party services, and it does not turn a source indicator into a vulnerability finding.
