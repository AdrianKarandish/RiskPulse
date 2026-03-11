# RiskPulse

RiskPulse is a Python CLI plus Streamlit web app for single-ticker risk analysis against the S&P 500 benchmark. It fetches historical prices with `yfinance`, computes downside and volatility metrics, writes CSV outputs, and renders charts into `outputs/` by default.

## Quick Start

Create a local virtual environment and install the declared dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Run the test suite:

```bash
.venv/bin/python -m pytest -q
```

Launch the Streamlit web app:

```bash
PYTHONPATH=src .venv/bin/streamlit run app.py
```

Run a rolling-window analysis:

```bash
PYTHONPATH=src .venv/bin/python -m riskpulse --ticker AAPL --rolling-days 60
```

Run a fixed date range:

```bash
PYTHONPATH=src .venv/bin/python -m riskpulse --ticker MSFT --start-date 2024-01-01 --end-date 2024-06-30
```

## How To Change Inputs

Change the ticker:

```bash
PYTHONPATH=src .venv/bin/python -m riskpulse --ticker NVDA --rolling-days 90
```

Change the date range:

```bash
PYTHONPATH=src .venv/bin/python -m riskpulse --ticker AMZN --start-date 2023-07-01 --end-date 2024-07-01
```

Change the output directory:

```bash
PYTHONPATH=src .venv/bin/python -m riskpulse --ticker META --rolling-days 30 --output-dir custom_outputs
```

## Outputs

RiskPulse writes four artifacts per run to `outputs/` unless `--output-dir` is provided:

- `riskpulse_main_<ticker>_<start>_<end>.csv`: aligned price history plus daily and cumulative returns.
- `riskpulse_prices_<ticker>_<start>_<end>.csv`: price-only export for the stock and benchmark.
- `riskpulse_cumulative_<ticker>_<start>_<end>.png`: cumulative return comparison chart.
- `riskpulse_volatility_<ticker>_<start>_<end>.png`: rolling annualized volatility chart.

The CLI also prints a JSON summary to stdout with:

- the normalized ticker
- the exact analyzed start and end dates
- period returns
- all computed metrics
- warnings
- artifact locations

The Streamlit app also provides:

- rolling-window or custom-date analysis inputs
- live benchmark return comparison against `^GSPC`
- interactive cumulative-return and rolling-volatility charts
- download buttons for main, price-only, and summary CSV exports
- inline validation and runtime error reporting

## Validation And Failure Modes

- Tickers must be 1-5 characters and use letters, numbers, dots, or dashes.
- Rolling windows must be between 5 and 252 business days.
- `--start-date` and `--end-date` must use `YYYY-MM-DD`, cannot be future dates, and must form an increasing range.
- `--output-dir` must either not exist yet or already be a directory.
- Analysis requires at least 2 overlapping trading days between the selected ticker and the benchmark after price cleanup.
- Empty or malformed downloaded price frames fail fast with explicit `ValueError` messages instead of producing partial outputs.
- The web app clears stale results after a failed run so an old analysis is not shown after an error.

## Module Responsibilities

- [src/riskpulse/main.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/main.py): CLI entrypoint, date-window resolution, stdout JSON payload.
- [app.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/app.py): Streamlit entrypoint, form handling, metrics/cards/charts/download rendering.
- [src/riskpulse/cli/parser.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/cli/parser.py): command parsing and cross-argument validation.
- [src/riskpulse/cli/validators.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/cli/validators.py): ticker, date, rolling-window, and output-path validation helpers.
- [src/riskpulse/data/market_data.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/data/market_data.py): market-data download, normalization, alignment, and overlap checks.
- [src/riskpulse/analytics/metrics.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/analytics/metrics.py): risk and performance metric calculations.
- [src/riskpulse/services/analysis_service.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/services/analysis_service.py): orchestration of fetch, metric computation, export, and artifact validation.
- [src/riskpulse/web/app_support.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/web/app_support.py): shared web-app helpers for request building, formatting, downloads, and Plotly chart construction.
- [src/riskpulse/reporting/csv_exporter.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/csv_exporter.py): CSV export shaping.
- [src/riskpulse/reporting/charts.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/charts.py): chart rendering.
- [src/riskpulse/reporting/filenames.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/filenames.py): deterministic artifact naming.
- [src/riskpulse/reporting/validation.py](/Users/adriankarandish/.openclaw/workspace/riskpulse/src/riskpulse/reporting/validation.py): validation of selected frames, metrics, and generated artifacts.

## Metrics

- Period return for stock and benchmark
- 1-year max drawdown
- Worst day return
- Worst 5-day return
- Parametric VaR 95%
- Historical VaR 95%
- CVaR 95%
- Annualized volatility
- Sortino ratio
- Beta
- Downside beta
- Piotroski F-score when fundamentals are available

## Additional Docs

- [docs/architecture.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/docs/architecture.md)
- [docs/configuration.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/docs/configuration.md)
- [docs/requirements-matrix.md](/Users/adriankarandish/.openclaw/workspace/riskpulse/docs/requirements-matrix.md)
