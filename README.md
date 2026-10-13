# Palm92 RepoGuard

**Human-governed repository agent for safer software after AI writes the code.**

> **AI investigates. Humans decide. Evidence is the asset.**

RepoGuard inspects a repository, reasons about a requested change, proposes a minimal patch, runs verification, assesses risk and produces an auditable evidence trail before consequential action.

## GitLab Life After Code adaptation

This branch adapts the existing RepoGuard project for GitLab Life After Code. RepoGuard predates the hackathon; this repository does not claim otherwise. The competition work focuses on the post-generation path from code to trustworthy production action.

**Governed path**

`REQUEST -> REPOSITORY SCAN -> PLAN -> PATCH PREVIEW -> TEST -> RISK CHECK -> HUMAN GATE -> ACTION -> EVIDENCE`

Core rule: **Access does not equal authority.**

The adaptation adds:
- `AGENTS.md` project instructions for governed agent behaviour;
- GitLab CI tests plus durable evidence artifacts;
- explicit safe/bounded and risky/escalation demo scenarios;
- an MIT licence;
- a GitLab migration and evidence plan in `docs/LIFE-AFTER-CODE.md`.

## Why it matters

Generating code is only part of software delivery. A production workflow also needs to answer:
- Was the repository understood before editing?
- Is the proposed change within scope?
- Did verification actually run?
- What risk did the change introduce?
- Who had authority to approve it?
- Can a reviewer reconstruct what happened later?

RepoGuard treats those questions as part of the engineering workflow rather than an afterthought.

## Existing RepoGuard capabilities

- repository reading and search
- structured plan-before-edit behaviour
- patch proposals and unified diff previews
- bounded repository tool loop
- test-feedback verification
- risk-aware human approval and rejection queue
- isolated benchmark copies
- evidence logging and experiment comparisons
- controlled Python benchmark tasks
- Gemma 4 adapter and experiment notebooks

## Run locally

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## GitLab CI

`.gitlab-ci.yml` runs the Python test suite and publishes JUnit plus a small evidence manifest containing the commit, pipeline and repository scope. A failed test remains visible; controls must not be removed merely to obtain a green pipeline.

## GitLab Duo Agent Platform

`AGENTS.md` supplies project-level governance instructions: inspect before editing, minimize diffs, test changes, preserve evidence, classify risk, and require human approval for consequential actions.

Real Duo execution evidence will only be claimed after the hackathon-provisioned GitLab project is available and the workflow has actually run there.

See `docs/LIFE-AFTER-CODE.md` for the migration, demo and evidence plan.

## Earlier research history

RepoGuard was previously developed for a Google Gemma 4 developer-agent experiment. That work remains useful evidence rather than being rewritten as if it were created for this hackathon.

The v0.7 Lite baseline recorded four controlled tasks, one fixed task, a 25% fix rate and 50% test pass rate. v0.8 tests automatic post-write verification with verified stopping. Experimental outputs belong under `artifacts/` and should be preserved unchanged when used as evidence.

## Licence

MIT. See `LICENSE`.

## Status

**Life After Code:** IN PROGRESS. GitLab-ready branch created; CI, governance instructions, licence and migration plan added. Waiting for the hackathon-provisioned GitLab project before claiming GitLab Duo execution or final submission.
