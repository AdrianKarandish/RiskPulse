# RiskPulse

RiskPulse is a modular Python CLI that calculates stock risk metrics, compares stock and benchmark performance, exports CSV outputs, and generates charts.

## Install

```bash
pip install -e .
```

## Usage

Rolling window:

```bash
python -m riskpulse --ticker AAPL --rolling-days 60
```

Custom date range:

```bash
python -m riskpulse --ticker MSFT --start-date 2024-01-01 --end-date 2024-06-30
```

Outputs are written to `outputs/` by default:

- `analysis_summary_<ticker>_<period>.csv`
- `price_history_<ticker>_<period>.csv`
- `cumulative_returns_<ticker>_<period>.png`
- `rolling_volatility_<ticker>_<period>.png`

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
- Piotroski F-score
