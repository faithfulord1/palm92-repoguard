# RepoGuard approval verification — 18 October 2026

## Target and scope

Existing draft PR #3, branch `forge/reject-stale-approval-20261015`.
Inspected source commit: `e06dc235d35ab36ca97a85fd3bb8f7628c307f7f`.
The PR was open and draft, with no discussion comments at inspection.
The other open PRs cover benchmarking and a GitLab adaptation; neither is
overwritten or merged by this change.

Operational problem: the existing stale-approval regression tests could not run
in an environment without pytest. A reviewer needs a free, repeatable way to
check the actual approval queue before accepting the draft change.

This addition changes tests and documentation only. It does not alter runtime
approval behaviour, grants, secrets, deployment, model execution or integrations.
All files changed by the tests are fictional and isolated in temporary directories.

## Reproduce

From the repository root, with its `src` directory on Python's import path:

```sh
PYTHONPATH=src python -m unittest discover -s tests -p test_review_stdlib.py -v
```

No package installation, network connection, API credentials, model or paid
service is required. This command selects only the new standard-library suite.
It does not collect pytest-based tests or claim that the full test suite ran.

## Executed evidence

- Python 3.12.14.
- `python -m pytest --version`: unavailable (`No module named pytest`).
- Focused standard-library suite: **12 tests passed, 0 failures, 0 errors**.
- Repeated the focused suite after the mutation experiment: **12 tests passed**.
- Regression-sensitivity experiment: removed the two stale-state checks only
  from the imported module's source in memory. **7 of 12 tests failed, 0 errors**.
  The seven failures covered deleted targets, changed content after character
  30000, newly created empty files, fresh-review recovery after a stale rejection,
  newly created populated files, same-length edits and competing proposals.
  No source file was modified by the mutation experiment.

The suite uses the real `ApprovalQueue` and `RepoTools`, not mock replacements.
It covers the existing preview/approval, rejection and two stale-path scenarios
plus deletion, long-file edits, empty-file creation, competing proposals, fresh
review recovery, approved creation and repeated-decision rejection.

## Limits and next action

DONE: the focused approval checks now have a dependency-free verification route.
WAITING: review of draft PR #3; no merge or deployment performed.
NEXT: run the complete pytest suite in an approved development/CI environment.

Passing these tests does not prove atomicity. Another process could still edit a
file between the final comparison and the write; filesystem locking/atomic
compare-and-write requires separate design and review. Symlink races, Unicode
normalisation and newline-byte preservation are not evaluated by this suite.
No production security or concurrency guarantee is made.

Free-first Plan A: the repository's existing pytest development dependency in
an approved environment. Plan B, executed here: the focused built-in unittest
command above. These are verification alternatives, not deployment failover.

Payment-failure behaviour in Verified Request remains outside this change and
awaits its existing approval gate. Telegram and WhatsApp were not tested here.
