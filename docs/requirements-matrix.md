# Requirements Matrix

This matrix is mapped against the original prompt now stored in `docs/original_requirements.md`, plus the current implementation and test evidence.

| Requirement | Status | Implementation | Tests | Notes |
|-------------|--------|----------------|-------|-------|
| CLI accepts ticker input | Done | `src/riskpulse/cli/parser.py`, `src/riskpulse/cli/validators.py` | `tests/unit/test_cli.py` | Includes normalization to uppercase. |
| CLI supports rolling-day analysis | Done | `src/riskpulse/cli/parser.py`, `src/riskpulse/main.py` | `tests/unit/test_cli.py` | Validated range `5-252`. |
| CLI supports fixed start/end date analysis | Done | `src/riskpulse/cli/parser.py`, `src/riskpulse/main.py` | `tests/unit/test_cli.py` | Requires both dates and validates ordering. |
| Invalid future dates fail fast | Done | `src/riskpulse/cli/validators.py` | `tests/unit/test_cli.py` | Explicit error message. |
| Invalid output path fails fast | Done | `src/riskpulse/cli/validators.py`, `src/riskpulse/services/validation.py` | `tests/unit/test_cli.py`, `tests/unit/test_validation.py` | Rejects existing files passed as output directories. |
| Historical price data fetched for ticker | Done | `src/riskpulse/data/market_data.py` | `tests/integration/test_pipeline_offline.py` | Production path uses `yfinance`. |
| Benchmark comparison against S&P 500 | Done | `src/riskpulse/domain/models.py`, `src/riskpulse/services/analysis_service.py` | `tests/integration/test_pipeline_offline.py` | Default benchmark is `^GSPC`. |
| Price data normalized before analysis | Done | `src/riskpulse/data/market_data.py` | `tests/unit/test_market_data.py` | Coerces dates/prices, drops duplicates and bad rows. |
| Insufficient overlap is rejected clearly | Done | `src/riskpulse/data/market_data.py` | `tests/unit/test_market_data.py`, `tests/integration/test_pipeline_offline.py` | Requires at least 2 shared trading days. |
| Risk metrics are computed | Done | `src/riskpulse/analytics/metrics.py`, `src/riskpulse/services/analysis_service.py` | `tests/unit/test_metrics.py`, `tests/integration/test_pipeline_offline.py` | Includes VaR, CVaR, drawdown, beta, volatility, Sortino. |
| Fundamentals-based Piotroski score handled gracefully | Done | `src/riskpulse/services/analysis_service.py`, `src/riskpulse/analytics/metrics.py` | `tests/integration/test_pipeline_offline.py` | Emits warning when unavailable. |
| Main analysis CSV is exported | Done | `src/riskpulse/reporting/csv_exporter.py`, `src/riskpulse/reporting/filenames.py` | `tests/integration/test_pipeline_offline.py` | Output path validated after write. |
| Price-only CSV is exported | Done | `src/riskpulse/reporting/csv_exporter.py`, `src/riskpulse/reporting/filenames.py` | `tests/integration/test_pipeline_offline.py` | Output path validated after write. |
| Cumulative return chart is exported | Done | `src/riskpulse/reporting/charts.py`, `src/riskpulse/reporting/filenames.py` | `tests/integration/test_pipeline_offline.py` | Headless-safe `Agg` backend. |
| Rolling volatility chart is exported | Done | `src/riskpulse/reporting/charts.py`, `src/riskpulse/reporting/filenames.py` | `tests/integration/test_pipeline_offline.py` | Uses 20-day rolling std. |
| Service validates payload integrity before returning | Done | `src/riskpulse/reporting/validation.py` | `tests/unit/test_validation.py` | Covers selected frame, metrics, and artifact paths. |
| Docs explain module responsibilities | Done | `README.md`, `docs/architecture.md` | Manual | Added explicit module map. |
| Docs explain how to run and change ticker/date | Done | `README.md`, `docs/configuration.md` | Manual | Includes `python3`/`.venv` commands. |
| Docs explain output locations and names | Done | `README.md`, `docs/configuration.md` | Manual | Matches current filename helpers. |
