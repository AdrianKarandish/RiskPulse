# Iteration 4 — Codex Plan (Planning Only)

## Goal
Deliver a real interactive web app for RiskPulse (not static file listing): input ticker/date mode, run analysis live via yfinance, show full metrics + benchmark comparison, render charts, and provide CSV downloads.

## Plan
1. Add a web app layer (Streamlit) that wraps existing analysis service.
2. Build input form:
   - ticker
   - rolling-days OR custom start/end
   - run button
3. On run, execute live analysis and keep result in session state.
4. Render output sections:
   - metric cards/table (all required metrics)
   - stock vs benchmark returns
   - selected-period dataframe preview
   - charts
5. Expose download buttons for main CSV and price-only CSV from current run artifacts.
6. Add robust error handling for:
   - invalid inputs
   - no data
   - no overlap
   - fundamentals missing (warning only)
   - upstream fetch failures
7. Keep CLI intact.
8. Add/adjust tests and update README with web run command.

## Acceptance
- User can complete full journey in browser: input -> run -> see metrics/charts -> download CSVs.
- Live yfinance path works when network is available.
- Failures surface cleanly without broken UI.
