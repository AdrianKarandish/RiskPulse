# Iteration 2 Execution Report

## Scope Executed

Executed Iteration 2 against `iteration2_claude_plan.md` using the current RiskPulse codebase as the source of truth for actual module names and responsibilities.

## Exact Changes

### Code

- Added output-directory validation in [src/riskpulse/cli/validators.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/cli/validators.py) and wired it into [src/riskpulse/cli/parser.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/cli/parser.py).
- Strengthened market-data normalization in [src/riskpulse/data/market_data.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/data/market_data.py):
  - validates required `Date` and `price` columns
  - coerces and cleans dates/prices
  - drops duplicate dates
  - rejects empty cleaned frames
  - rejects invalid fetch ranges
  - rejects selected windows with fewer than 2 overlapping trading days
- Added request-level validation in [src/riskpulse/services/validation.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/services/validation.py).
- Added result/artifact validation in [src/riskpulse/reporting/validation.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/validation.py).
- Fixed stale filename helpers in [src/riskpulse/reporting/filenames.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/filenames.py) so they match the current `AnalysisRequest` model and actual output naming scheme.
- Updated [src/riskpulse/services/analysis_service.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/services/analysis_service.py) to:
  - validate requests before execution
  - validate selected analysis frames
  - validate metrics payload completeness/finite values
  - use centralized artifact filename helpers
  - validate that exported artifacts were actually created
  - improve the Piotroski warning text

### Tests

- Expanded CLI coverage in [tests/unit/test_cli.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/tests/unit/test_cli.py) for:
  - missing `--end-date`
  - illegal `--end-date` with `--rolling-days`
  - future-date rejection
  - output path pointing to a file
- Added [tests/unit/test_market_data.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/tests/unit/test_market_data.py) for overlap, required-column, and normalization/deduplication behavior.
- Added [tests/unit/test_validation.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/tests/unit/test_validation.py) for request validation, selected-frame validation, metric finiteness checks, and artifact existence checks.
- Extended [tests/integration/test_pipeline_offline.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/tests/integration/test_pipeline_offline.py) with an empty-selected-window failure case.

### Documentation

- Rewrote [README.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/README.md) with:
  - quick start using `python3` and `.venv`
  - explicit run commands
  - how to change ticker, date range, and output directory
  - output filenames and locations
  - validation/failure-mode notes
  - module responsibilities
- Added [docs/architecture.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/docs/architecture.md).
- Added [docs/configuration.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/docs/configuration.md).
- Added [docs/requirements-matrix.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/docs/requirements-matrix.md). Since the original prompt text is not present in the repo, the matrix was derived from the visible CLI/product scope plus `iteration2_claude_plan.md`.

## Commands Run And Results

### Environment Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Result: succeeded.

### Test Run

```bash
.venv/bin/python -m pytest -q
```

Result: succeeded.

Exact outcome:

```text
18 passed in 8.89s
```

### Sample Command

```bash
PYTHONPATH=src .venv/bin/python -m riskpulse --ticker AAPL --start-date 2024-01-02 --end-date 2024-03-01
```

Result: failed because the environment could not resolve Yahoo Finance hosts during the live `yfinance` download.

Observed error summary:

```text
Failed to get ticker 'AAPL' ... Could not resolve host: guce.yahoo.com
ValueError: No data for AAPL
```

No output artifacts were produced from the sample run because price download failed before export.

## Issues / Follow-Up

- Live CLI runs depend on outbound DNS/network access to Yahoo Finance. In this environment, that access was unavailable, so only the offline monkeypatched integration path could be executed successfully.
- Matplotlib warned that `/Users/adriankarandish/.matplotlib` was not writable and created a temporary cache directory. This did not affect tests, but setting `MPLCONFIGDIR` to a writable path would remove the warning in constrained environments.
