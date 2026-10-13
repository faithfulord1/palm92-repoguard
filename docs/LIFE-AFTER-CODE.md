# Life After Code: RepoGuard + Governed Agent

## Challenge framing
AI can generate code quickly. The production problem begins after generation: what may be changed, who authorizes it, what evidence proves it was tested, and what happens when risk is too high?

Palm92 RepoGuard adds a governed post-code path:

`REQUEST -> REPOSITORY SCAN -> PLAN -> PATCH PREVIEW -> TEST -> RISK CHECK -> HUMAN GATE -> ACTION -> EVIDENCE`

The core rule is: **access does not equal authority**.

## Existing project vs hackathon work
RepoGuard predates Life After Code and was originally developed as a repository-aware, human-governed coding agent and research project. The Life After Code adaptation does not conceal that history. Hackathon-specific work is isolated on the `gitlab-life-after-code` branch and is intended to be moved into the provisioned GitLab project.

### Existing before this adaptation
- repository inspection and search
- patch proposals and diff previews
- tests and benchmark tasks
- risk-aware human approval
- evidence logging
- Gemma experiment notebooks

### Added for Life After Code
- GitLab CI pipeline with test evidence artifacts
- `AGENTS.md` governance instructions for GitLab Duo-compatible agent context
- explicit post-generation production governance framing
- MIT licence
- GitLab migration/runbook and evidence checklist

## GitLab Duo design
GitLab Duo can consume project instructions from `AGENTS.md`. RepoGuard uses that file to require inspection, minimal diffs, tests, evidence, risk classification and human approval for consequential changes.

When the hackathon-provisioned GitLab project is available, the implementation path is:
1. import/mirror the open-source RepoGuard project;
2. run `.gitlab-ci.yml` on the GitLab runner;
3. enable the hackathon-provided Duo Agent Platform capabilities;
4. use RepoGuard governance instructions with Duo;
5. capture agent session, merge request, pipeline and evidence artifacts;
6. demonstrate one safe change and one blocked/escalated change.

## Demo acceptance tests
### Scenario A: safe, bounded fix
Expected: inspect -> propose -> tests pass -> LOW risk -> evidence -> approved action.

### Scenario B: broad or risky request
Expected: detect scope/risk -> do not silently execute -> require human approval or reject -> preserve evidence.

### Scenario C: failing verification
Expected: pipeline/test failure remains visible; the agent must not bypass or delete the control merely to get green status.

## Evidence to capture in GitLab
- source commit SHA
- issue/request
- Duo agent/session output
- proposed diff or merge request
- CI pipeline result
- JUnit report
- evidence artifact
- human approve/reject decision
- final commit/deployment status

## Plan B
If Duo or hackathon provisioning is delayed, keep the GitLab-ready branch and CI configuration as the reproducible baseline. Do not invent Duo execution evidence. Move the branch to the provisioned GitLab project when access is granted, then run and capture the real evidence.
