# Iteration 4 Execution Report

## Scope Executed
Implemented the Streamlit web app requested for RiskPulse while preserving the existing CLI flow and reusing the current analysis service.

## Exact Changes
1. Added web app dependencies:
   - `requirements.txt`
   - `pyproject.toml`
   - Added `plotly>=5.15`
   - Added `streamlit>=1.28`
2. Added the interactive Streamlit app:
   - `app.py`
   - Supports ticker input, rolling-window or custom-date selection, a run button, live analysis execution, benchmark return comparison, charts, CSV downloads, warnings, and error states.
3. Added a testable web support layer:
   - `src/riskpulse/web/__init__.py`
   - `src/riskpulse/web/app_support.py`
   - Centralizes request normalization, metric formatting, CSV byte generation, and Plotly figure construction.
4. Added automated tests for the new web layer:
   - `tests/unit/test_web_app_support.py`
   - Covers rolling/custom request building, validation failures, CSV export helpers, metrics table formatting, and chart builders.
5. Updated docs:
   - `README.md`
   - Added Streamlit launch instructions and documented web-app capabilities.

## Commands Run
1. Test suite:
   - `PYTHONPATH=src .venv/bin/python -m pytest -q`
   - Result: `23 passed, 1 skipped in 9.34s`
2. Dependency install attempt for web app smoke check:
   - `.venv/bin/pip install 'plotly>=5.15' 'streamlit>=1.28'`
   - Result: failed due sandbox/network DNS resolution to PyPI
3. Streamlit smoke check attempt:
   - `PYTHONPATH=src .venv/bin/streamlit run app.py --server.headless true`
   - Result: failed because `.venv/bin/streamlit` is not present

## Results
- CLI behavior remains covered by the existing CLI and integration tests.
- Web app implementation is present and wired to the live `run_analysis` service.
- The new unit tests passed.
- One test was skipped because `plotly` is not installed in the current offline sandbox.

## Issues / Constraints
- A live Streamlit smoke check could not be completed in this environment because:
  - `streamlit` is not installed in `.venv`
  - the sandbox cannot reach PyPI to install new packages
- The attempted smoke-check command failed immediately:
  - `PYTHONPATH=src .venv/bin/streamlit run app.py --server.headless true`
  - shell error: `no such file or directory: .venv/bin/streamlit`

## Notes
- The web helper module uses lazy `plotly` imports so the non-web test suite can still run in environments where web dependencies are not installed yet.
- The web app clears stale analysis results after failed runs so old results are not shown after an error.
