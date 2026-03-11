# Configuration Reference

RiskPulse is configured through CLI flags rather than a config file.

## Required Inputs

- `--ticker <symbol>`: stock ticker to analyze.
- One period mode:
  - `--rolling-days <5-252>`
  - `--start-date YYYY-MM-DD --end-date YYYY-MM-DD`

## Optional Inputs

- `--output-dir <path>`: output directory. Default: `outputs`.
- `--verbose`: increases logging verbosity. Repeat for more detail.

## Defaults

- Benchmark: `^GSPC`
- Output directory: `outputs/`
- Volatility chart rolling window: 20 trading days
- Risk-free rate for Sortino: 0

## Valid Ranges And Constraints

- Ticker: 1-5 characters, letters/numbers/dot/dash only.
- Rolling window: 5-252 business days.
- Dates: `YYYY-MM-DD`, not in the future, and start must be earlier than end.
- Output path: must be a directory if it already exists.

## Failure Modes

- No downloaded price data: the run fails with `No data for <ticker>`.
- Malformed downloaded frames: the run fails if `Date` or `price` columns cannot be normalized.
- Insufficient overlap: the run fails if the selected ticker and benchmark do not share at least 2 trading days in the chosen window.
- Missing fundamentals: the run still succeeds, but `piotroski_f_score` becomes `null` and a warning is emitted.
