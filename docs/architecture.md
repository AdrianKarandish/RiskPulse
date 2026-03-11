# Architecture

## Data Flow

`CLI args -> validation -> date window resolution -> price fetch -> frame alignment -> metrics -> CSV/chart export -> stdout JSON`

## Module Responsibilities

- [src/riskpulse/main.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/main.py): resolves the effective analysis period, builds `AnalysisRequest`, prints the final JSON payload.
- [src/riskpulse/domain/models.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/domain/models.py): dataclasses shared across CLI, service, and reporting layers.
- [src/riskpulse/cli/parser.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/cli/parser.py): CLI flag definitions and cross-flag validation.
- [src/riskpulse/cli/validators.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/cli/validators.py): primitive validation helpers.
- [src/riskpulse/services/validation.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/services/validation.py): request-level guardrails before network or filesystem work begins.
- [src/riskpulse/data/market_data.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/data/market_data.py): downloads historical prices and normalizes them into clean `Date` and `price` columns.
- [src/riskpulse/analytics/metrics.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/analytics/metrics.py): pure metric calculations over aligned pandas series.
- [src/riskpulse/reporting/csv_exporter.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/csv_exporter.py): exports analysis tables as CSV.
- [src/riskpulse/reporting/charts.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/charts.py): renders cumulative-return and rolling-volatility charts.
- [src/riskpulse/reporting/filenames.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/filenames.py): centralizes artifact naming conventions.
- [src/riskpulse/reporting/validation.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/validation.py): ensures the selected frame, metrics payload, and artifact paths are complete and sane.

## Operational Notes

- The CLI defaults to benchmark `^GSPC`.
- Rolling windows back into calendar days by multiplying the requested business-day window by `1.6`.
- The service fetches an extended history window to support metrics such as 1-year max drawdown even when the selected window is shorter.
- Charts use the non-interactive `Agg` backend, so the tool works in headless environments.

## Edge-Case Matrix

| Scenario | Expected behavior |
|---|---|
| Invalid ticker format | Fail fast with validation error from CLI validator |
| Rolling days outside allowed range | Fail fast with clear range message |
| Start date >= end date | Fail fast before fetch |
| Output path is an existing file | Fail fast with directory error |
| Yahoo returns empty dataset | Raise `No data for <ticker>` |
| Missing/dirty `Date` or `price` columns | Normalize when possible; raise explicit column/usable-data error when not possible |
| Stock/benchmark no overlap in selected range | Raise overlap error; do not emit partial CSV/chart artifacts |
| Fundamentals unavailable for Piotroski | Continue run; set Piotroski null and append warning |
| Insufficient sample for a metric | Metric may be null; run still completes if core frame is valid |
| DNS/network failure to upstream | Run fails with surfaced upstream error; no fake outputs |
