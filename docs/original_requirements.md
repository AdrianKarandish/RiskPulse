# Original Requirements (Verbatim)

Prompt used for RiskPulse:

"Goal:
Create a tool where I can enter a stock ticker and a custom analysis period, then generate risk metrics, return comparisons, CSV exports, and charts.

Requirements:

1. Inputs
- Accept a stock ticker
- Accept either:
 - a rolling window (example: last 10 trading days), or
 - a custom start date and end date

2. Data
- Pull historical price data for:
 - the selected stock
 - the S&P 500 benchmark for the same period
- Use the benchmark as the default comparison index

3. Metrics to calculate
- Max Drawdown (1Y)
- Worst 5-Day
- VaR 95% (Parametric)
- Beta
- Annualized Volatility
- Piotroski F-Score
- Worst Day
- VaR 95% (Historical)
- CVaR 95% (1D)
- Downside Beta (B⁻)
- Sortino

4. Return analysis
- Compute the stock’s actual return over the selected period
- Compute the S&P 500 benchmark return over the same period
- Allow direct comparison of stock return vs benchmark return

5. CSV outputs
Generate a main CSV report for the selected period containing:
- Date
- Stock price
- Stock daily return
- Stock cumulative return
- Benchmark price
- Benchmark daily return
- Benchmark cumulative return

Also generate a separate price-only CSV for the selected period containing:
- Date
- Stock price
- Benchmark price

6. Charts
Generate:
- one chart showing stock cumulative return vs S&P 500 cumulative return for the selected period
- one separate chart showing volatility for the selected period

7. Functional expectations
- The analysis period must be configurable, not hardcoded
- The tool should work for any stock ticker
- The output should be clean and easy to read
- Structure the project cleanly, with separate parts for:
 - data retrieval
 - metric calculation
 - return comparison
 - CSV export
 - chart generation

8. Deliverable
Please build this as a clean, modular project and explain:
- file structure
- what each module does
- how to run it
- how to change ticker and date range
- where the CSV outputs are saved
- where the charts are saved

If any metric cannot be computed directly from the selected short window, use the necessary longer historical data in the background while still reporting the selected analysis period separately."
