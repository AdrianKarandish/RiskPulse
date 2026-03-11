# Iteration 1 — Codex Plan (Planning Only)

## Objective
Build RiskPulse: a modular stock risk analytics tool where user inputs a ticker plus either a rolling window or custom start/end dates, then gets risk metrics, stock-vs-benchmark return comparison, CSV exports, and charts.

## Assumptions
- Python CLI app (3.12+)
- Data source: yfinance for stock + benchmark (^GSPC)
- Selected period is always reported as requested
- If needed, longer lookback is fetched in background for specific metrics (e.g., 1Y max drawdown)
- Missing data returns NA + warnings

## Architecture
- CLI layer: argument parsing + validation
- Data layer: selected-period and extended-lookback fetch, preprocessing/alignment
- Analytics layer: returns, risk metrics, beta/downside beta, Piotroski, summary
- Reporting layer: CSV exporters + charts
- Service layer: orchestration of full run
- Tests mirror modules with fixtures

## File Tree
- `src/riskpulse/main.py`
- `src/riskpulse/cli/{parser.py,validators.py}`
- `src/riskpulse/domain/models.py`
- `src/riskpulse/data/{market_data.py,fundamentals.py,preprocess.py}`
- `src/riskpulse/analytics/{returns.py,risk_metrics.py,beta.py,fundamentals.py,summary.py}`
- `src/riskpulse/reporting/{csv_exporter.py,charts.py,filenames.py}`
- `src/riskpulse/services/analysis_service.py`
- `src/riskpulse/utils/{dates.py,logging.py,math_utils.py}`
- `tests/*` + fixtures
- `outputs/`

## Implementation Steps
1. Scaffold package + dependencies
2. Build CLI inputs (ticker + rolling OR custom range)
3. Date utilities for selected + extended lookbacks
4. Domain models
5. Market/fundamental data fetchers
6. Preprocess/alignment and return series
7. Risk metrics: max drawdown 1Y, worst day/5-day, VaR95 param/hist, CVaR95, ann vol, Sortino
8. Beta + downside beta
9. Return comparison stock vs benchmark
10. Piotroski F-score + fallback rules
11. CSV exports (main + price-only)
12. Chart generation (cumulative returns + volatility)
13. Orchestration service + warnings
14. Unit + integration tests
15. README usage and output locations

## Test Plan
- CLI/date validation tests
- Metric formula tests on synthetic known-series data
- Export schema/content tests
- Chart file creation tests
- Integration tests for service pipeline with fixtures
- Manual smoke test on live ticker

## Risks
- Inconsistent fundamentals for Piotroski
- Short windows may be insufficient for stable metrics
- yfinance endpoint variability
- Benchmark (^GSPC) is price index, not total return

## Acceptance Criteria
- Works for any ticker with rolling/custom period
- Computes required metrics (or explicit NA/warnings)
- Computes stock vs benchmark period returns
- Produces both CSVs
- Produces both charts
- Modular project structure with clear separation of concerns
