# RepoGuard submission draft and evidence checklist

**Status, 26 September 2026:** Draft only. The [official main-track overview](https://www.kaggle.com/competitions/gemma-4-developer-agent) specifies a `submission.zip` containing an ADK-compatible `agent.yaml` at the archive root. It supports only `gemma-4-31b-it-qat-w4a16-ct` for every agent and subagent, with optional LoRA adapters. The agent may request only harness tools and custom subagents via `agent_tool`. Patches are judged by validation tests, and the total agent budget is 12 hours. The entry and team merger deadline is 25 November 2026; final submission is 2 December 2026, 23:59 UTC unless organizers revise it. Faith must accept the competition rules by the entry deadline. Check the signed-in Rules page and dataset `HARNESS_README.md` for the exact config schema and eligibility before submission. The [optional paper track](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper) has a separate 12 November 2026 deadline.

**Critical validation gap:** The Python agent and E4B Colab notebook are separate from the ADK candidate. The E4B benchmark cannot serve as an official 31B harness evaluation. Test the ADK candidate against the competition harness; preserve the earlier experiments as development evidence.

## ADK candidate prepared

The separate `competition/adk_submission/` directory contains a minimal declarative 31B agent, its prompt and a per-task budget. Build with `python scripts/build_adk_submission.py`; the archive is generated at `submission.zip` and excluded from Git. Local checks verify the ZIP layout, model name, tool list and YAML parsing. The root agent and evaluation fields were compared with the official dataset's `sample_submission/agent.yaml` and `sample_submission/eval_config.yaml` downloaded on 26 September 2026. The sample's LoRA adapter and analyzer subagent are optional and are intentionally absent. **This is a candidate, not a scored or compiler-validated submission.** The `adk-submission` validator and an official inference run remain necessary to establish runtime compatibility and performance. The configured 5-minute per-task ceiling is a budget hypothesis for roughly 120 hidden tasks under the 12-hour global limit, not a measured optimum.

## Kaggle upload handoff

The ZIP contains only `agent.yaml`, `eval_config.yaml`, and `prompts/system.md`, with `agent.yaml` at its root. In Faith's signed-in competition page, choose **Submit Prediction**, select this `submission.zip`, and complete the site's submission flow. Preserve the Kaggle submission ID and any validation errors or scoring output for the evidence table. Do not label the entry as successful until Kaggle reports acceptance. The browser available to the engineering session was signed out and its Kaggle login page failed with an anti-forgery token error; Faith's signed-in desktop browser is a separate session.

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
- Validate the prepared archive with the official `adk-submission` compiler and competition evaluation harness when available; compare the recorded score and errors with the candidate configuration.
- Run medium-v002 only with available GPU, preserve its raw JSONL and summary under a new experiment folder, and review logs for secrets before publication.
- Record task-level initial tests, model actions, proposals, approvals, applied diffs, final tests, steps, timing and failures from actual evidence.
- Update the table and video claims only after verifying the archived files. Obtain Faith's approval before the external competition submission.
