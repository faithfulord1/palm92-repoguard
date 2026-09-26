# RepoGuard submission draft and evidence checklist

**Status, 26 September 2026:** Draft only. The official Kaggle competition page is [Gemma 4 Developer Agent](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview/description). Its full rules, eligibility, deadline, evaluation and upload format were not accessible from this environment. Verify them in the signed-in Kaggle interface before tailoring or submitting this package. The separate paper track has separate requirements.

## Project description

Palm92 RepoGuard explores whether a compact Gemma 4 model can repair small Python repository defects with structured reading, bounded actions, risk review and test feedback. It runs tasks in disposable repository copies, logs proposed actions, requires approval for sensitive paths, and only counts an applied fix when the post-change tests pass. The published evidence includes an unsuccessful three-task initial medium run and a successful single-task invoice diagnostic. The broader follow-up awaits a GPU run.

## Evidence table

| Experiment | Task pack | Tasks | Verified repairs | Evidence and limits |
| --- | --- | ---: | ---: | --- |
| medium-v001 | authored medium | 3 | 0 | Archived summary and JSONL; all reached 12 steps; raw model actions absent. |
| diagnostic-v002 | authored invoice only | 1 | 1 | 4 model actions, 1 normal-risk approved write, 3/3 tests passed; no repeated read attempted. |
| medium-v002 | authored medium | 3 planned | Pending | Colab notebook ready; no archived results. |

Do not calculate a combined success percentage across these overlapping tasks or the easier v0.7/v0.8 pack.

## Demonstration video script, about 90 seconds

1. Show the three failing fixture checks and explain that they establish starting defects.
2. Open the invoice diagnostic audit: source and test reads, proposed change, approval, then passing post-write tests.
3. Show the agent's repeated-read guard test and its refusal to accept an unverified `fixed` claim.
4. Show the Colab notebook's GPU preflight and archived evidence folder. Say clearly that medium-v002 is pending if it has not completed.
5. Close with the limits: authored visible tests, trusted disposable fixture repositories, human oversight for sensitive changes.

## Before entry

- Confirm current official Kaggle rules, eligibility, dates, required runtime/interface, judging criteria, and submission artifact format in the signed-in account.
- Run medium-v002 only with available GPU, preserve its raw JSONL and summary under a new experiment folder, and review logs for secrets before publication.
- Record task-level initial tests, model actions, proposals, approvals, applied diffs, final tests, steps, timing and failures from actual evidence.
- Update the table and video claims only after verifying the archived files. Obtain Faith's approval before the external competition submission.
