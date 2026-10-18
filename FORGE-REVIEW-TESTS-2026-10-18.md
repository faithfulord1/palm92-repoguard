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

## Full-suite follow-up — 18 October 2026

The pytest dependency blocker above was subsequently resolved in an isolated
virtual environment. Source was checked out from the exact draft commit
`72d4646172477a3632044b61f3fd7e6b226efd63` before changes. No AGENTS.md existed
in that commit's recursive file tree. Installed pytest 9.1.1 and its development
dependencies; no Gemma, Torch, live API or model download was used.

Initial complete suite: **26 passed, 1 failed**. The failure was the scripted
agent retry test: a quick same-size source edit could reuse timestamp-based
bytecode from the prior test invocation, leaving a corrected source file tested
as if it still contained the previous bug.

Added a deterministic regression that compiles the old source, rewrites it with
the same size, restores its original timestamp and checks the test subprocess
imports the new value. Before the fix it failed with the old value. A second
new check confirmed that the default command should use the running interpreter,
not whichever `python` happens to be first on PATH; that check also failed before
the fix.

Changed only `RepoTools.run_tests`: default to `sys.executable`, copy the parent
environment and give each subprocess a fresh temporary `PYTHONPYCACHEPREFIX`.
Existing repository caches are not deleted and the parent environment is not
modified. The temporary cache is cleaned up when the command returns or raises.
Custom commands, timeout and output payload remain supported. A custom Python
command that explicitly overrides or ignores this environment setting is outside
the protection provided here.

After the fix, the complete suite passed: **29 passed, 0 failed** on Python
3.12.14 with pytest 9.1.1. Command used (virtualenv Python on PATH for subprocess
consistency, external plugin autoload disabled):

```sh
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

`git diff --check` passed. Tests cover mock/scripted agents, benchmark isolation,
approval queues, reports, experiments, risk checks and repository tools. This
result supersedes the earlier statement that the full suite had not run.
The old baseline evidence above is retained for traceability.

DONE: full-suite dependency blocker resolved and stale-bytecode test-runner bug
fixed in the draft. WAITING: review and merge approval. No deployment, live
integration, real financial action or benchmark artefact modification occurred.
Approval-time filesystem race limitations remain as previously documented.
