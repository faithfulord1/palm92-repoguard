# Palm92 RepoGuard Agent Instructions

## Mission
Improve software safely after code is generated. AI investigates and proposes; humans decide consequential repository actions.

## Required workflow
1. Understand the issue and repository context.
2. Inspect before editing.
3. Propose the smallest viable change.
4. Run tests and security/policy checks.
5. Produce evidence: files inspected, proposed diff, tests, risk and rationale.
6. Classify risk LOW, MEDIUM or HIGH.
7. Require human approval for MEDIUM/HIGH risk, destructive, credential, deployment, dependency, permission or broad-scope changes.
8. Never bypass a failed control to make a pipeline pass.
9. Never expose secrets or sensitive data.
10. Record the final decision and test evidence.

## Commands
- Install dev dependencies: `python -m pip install -e '.[dev]'`
- Run tests: `pytest -q`

## Change discipline
- Prefer minimal diffs.
- Preserve existing tests and add regression tests for fixes.
- Do not claim a test passed unless it was executed.
- Do not claim deployment, certification or production readiness without evidence.

## Palm92 principle
Access does not equal authority. AI investigates. Humans decide. Evidence is the asset.
