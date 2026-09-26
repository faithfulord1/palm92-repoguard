# Palm92 RepoGuard

RepoGuard is an experimental Gemma 4 coding agent. It reads an isolated Python repository, proposes file replacements, gates sensitive changes, and checks approved changes with pytest. It is a research prototype, not a production security boundary.

**Competition validation gap:** The official main track requires an ADK `agent.yaml` submission with the specified Gemma 4 31B variant. The earlier Python/E4B exploration is separate from the new unscored ADK candidate. See [submission preparation](docs/SUBMISSION_DRAFT.md).

A separate **unscored ADK candidate** now lives in `competition/adk_submission/`. Build the upload archive with `python scripts/build_adk_submission.py`. It still needs validation against the Kaggle sample/harness and a real competition test; the historical E4B results do not measure this 31B agent.

## Current status

The `v0.9-hard-benchmarks` branch contains three authored medium tasks. Their original fixtures all fail their intended tests. The archived `medium-v001` run attempted all three, fixed zero, hit the 12-step limit each time, and lacks raw action traces. The separate `diagnostic-v002` invoice run proposed one change in four model actions and passed all three invoice tests after automatic approval. It did not exercise duplicate-read blocking. **The three-task `medium-v002` follow-up has not been run or validated.** Results from the easier v0.7/v0.8 pack are not comparable to these medium-task rates.

See [evidence and limitations](artifacts/v0.9/README.md), [architecture](docs/ARCHITECTURE.md), and [submission preparation](docs/SUBMISSION_DRAFT.md).

## Local setup and checks

Python 3.11 or newer is required. From the repository root:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts/check_v0_9_fixtures.py
```

The fixture checker succeeds only when each unmodified medium fixture fails its tests as expected. It does not demonstrate an agent repair. For a CPU-only demonstration, inspect the deterministic scripted model tests in `tests/test_agent.py` and run `python -m pytest -q tests/test_agent.py`.

## Gemma 4 follow-up in Colab

Open [medium-v002 follow-up](https://colab.research.google.com/github/faithfulord1/palm92-repoguard/blob/v0.9-hard-benchmarks/notebooks/RepoGuard_v0_9_Medium_v002_Followup.ipynb). Select a GPU runtime, run the cells in order, and download the evidence archive. The notebook checks CUDA before model execution. If the free GPU quota is exhausted, wait for access; do not label CPU checks as a Gemma benchmark. Use a distinct experiment ID if `medium-v002` evidence already exists.

The benchmark permits automatic approval only for normal-risk edits in disposable copies of the authored fixtures. The agent requires manual approval for other edits, and tests must pass after an applied change before a run can be called fixed. Review model action logs before sharing them.

## Layout

- `src/repoguard/`: agent, tools, approval, risk, audit, reporting, benchmark.
- `benchmarks/`: authored task definitions and defective fixture repositories.
- `notebooks/`: Colab experiment notebooks.
- `artifacts/`: preserved historical evidence; never overwrite an experiment ID.
- `docs/`: architecture, experiment plans, and competition draft.

## Limits

Three authored tasks with visible tests are too small for a general coding benchmark. Test success only verifies the available test suite. The file and approval controls are prototype controls, not isolation against hostile repository content or arbitrary test code; run only trusted fixtures in a disposable environment.
