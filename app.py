from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from riskpulse.web.app_support import (
    METRIC_SPECS,
    build_cumulative_figure,
    build_main_csv_bytes,
    build_metrics_table,
    build_price_csv_bytes,
    build_summary_csv_bytes,
    build_volatility_figure,
    run_web_analysis,
)


st.set_page_config(page_title="RiskPulse", page_icon="RP", layout="wide")


def _render_results() -> None:
    result = st.session_state["analysis_result"]
    selected = result.selected
    stock_return = result.period_returns.get("stock_period_return")
    benchmark_return = result.period_returns.get("benchmark_period_return")
    excess_return = None
    if stock_return is not None and benchmark_return is not None:
        excess_return = stock_return - benchmark_return

    st.subheader(f"{result.request.ticker} vs S&P 500")
    st.caption(
        f"Analyzed period: {result.request.start.date().isoformat()} to {result.request.end.date().isoformat()} | "
        f"Benchmark: {result.request.benchmark}"
    )

    for warning in result.warnings:
        st.warning(warning)

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Stock Return",
        "N/A" if stock_return is None else f"{stock_return:.2%}",
    )
    col2.metric(
        "Benchmark Return",
        "N/A" if benchmark_return is None else f"{benchmark_return:.2%}",
    )
    col3.metric(
        "Excess Return",
        "N/A" if excess_return is None else f"{excess_return:.2%}",
    )

    st.subheader("Risk Metrics")
    metric_columns = st.columns(3)
    for index, (label, key, kind) in enumerate(METRIC_SPECS):
        value = result.metrics.get(key)
        rendered = "N/A" if value is None else (f"{value:.2%}" if kind == "percent" else f"{value:.3f}")
        metric_columns[index % len(metric_columns)].metric(label, rendered)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(
            build_cumulative_figure(selected, ticker=result.request.ticker),
            use_container_width=True,
        )
    with chart_col2:
        st.plotly_chart(build_volatility_figure(selected), use_container_width=True)

    st.subheader("Downloads")
    dl1, dl2, dl3 = st.columns(3)
    period_suffix = f"{result.request.ticker}_{result.request.start.date()}_{result.request.end.date()}"
    dl1.download_button(
        "Main CSV",
        data=build_main_csv_bytes(selected),
        file_name=f"riskpulse_main_{period_suffix}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    dl2.download_button(
        "Prices CSV",
        data=build_price_csv_bytes(selected),
        file_name=f"riskpulse_prices_{period_suffix}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    dl3.download_button(
        "Summary CSV",
        data=build_summary_csv_bytes(result),
        file_name=f"riskpulse_summary_{period_suffix}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    with st.expander("Full metrics and artifact details"):
        st.dataframe(build_metrics_table(result), hide_index=True, use_container_width=True)
        st.json(
            {
                "warnings": result.warnings,
                "artifacts": result.artifacts,
            }
        )
        st.dataframe(selected, hide_index=True, use_container_width=True)


def main() -> None:
    st.title("RiskPulse")
    st.write("Interactive single-ticker risk analysis against the S&P 500 benchmark.")

    with st.form("analysis_form"):
        input_col1, input_col2 = st.columns([1, 2])
        ticker = input_col1.text_input("Ticker", value="AAPL", max_chars=5)
        mode = input_col2.radio(
            "Date Mode",
            options=["Rolling Window", "Custom Range"],
            horizontal=True,
        )

        rolling_days = None
        start_value = None
        end_value = None
        today = date.today()
        if mode == "Rolling Window":
            rolling_days = st.slider("Rolling Business Days", min_value=5, max_value=252, value=60)
        else:
            date_col1, date_col2 = st.columns(2)
            start_value = date_col1.date_input(
                "Start Date",
                value=today - timedelta(days=365),
                max_value=today,
            )
            end_value = date_col2.date_input(
                "End Date",
                value=today,
                max_value=today,
            )

        submitted = st.form_submit_button("Run Analysis", type="primary", use_container_width=True)

    if submitted:
        try:
            result = run_web_analysis(
                ticker=ticker,
                use_rolling_window=mode == "Rolling Window",
                rolling_days=rolling_days,
                start_date=start_value,
                end_date=end_value,
            )
        except ValueError as exc:
            st.session_state.pop("analysis_result", None)
            st.error(str(exc))
        except Exception as exc:
            st.session_state.pop("analysis_result", None)
            st.error(f"Analysis failed: {exc}")
        else:
            st.session_state["analysis_result"] = result
            st.success("Analysis complete.")

    if "analysis_result" in st.session_state:
        _render_results()
    else:
        st.info("Enter a ticker and date selection, then run an analysis.")


if __name__ == "__main__":
    main()
