# RiskPulse Iteration 4 - Execution Plan

## Implementation Order

### 1. Add Dependencies
**File**: `requirements.txt`
```diff
+ streamlit>=1.28.0
+ plotly>=5.15.0
```

### 2. Create Streamlit App
**File**: `app.py` (new)
```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io
from src.analysis_service import AnalysisService

st.set_page_config(page_title="RiskPulse", layout="wide")

def main():
    st.title("📊 RiskPulse - Stock Risk Analysis")
    
    # Input form
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            ticker = st.text_input("Stock Ticker", value="AAPL", help="e.g., AAPL, MSFT, GOOGL")
            
        with col2:
            mode = st.radio("Time Period", ["Rolling Days", "Custom Range"])
        
        if mode == "Rolling Days":
            rolling_days = st.slider("Days", 30, 1000, 252)
            start_date = end_date = None
        else:
            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
            with col4:
                end_date = st.date_input("End Date", datetime.now())
            rolling_days = None
            
        submitted = st.form_submit_button("Run Analysis", type="primary")
    
    if submitted:
        run_analysis(ticker, rolling_days, start_date, end_date)
    
    # Display results if available
    if 'results' in st.session_state:
        display_results()

def run_analysis(ticker, rolling_days, start_date, end_date):
    with st.spinner("Fetching data and running analysis..."):
        try:
            service = AnalysisService()
            
            if rolling_days:
                results = service.analyze_stock(ticker, rolling_days=rolling_days)
            else:
                results = service.analyze_stock(ticker, start_date=start_date.strftime('%Y-%m-%d'), 
                                              end_date=end_date.strftime('%Y-%m-%d'))
            
            st.session_state.results = results
            st.session_state.ticker = ticker
            st.success("Analysis complete!")
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            if 'results' in st.session_state:
                del st.session_state.results

def display_results():
    results = st.session_state.results
    ticker = st.session_state.ticker
    
    # Metrics cards
    st.subheader("📈 Risk Metrics")
    
    metrics = results.get('metrics', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sharpe Ratio", f"{metrics.get('sharpe_ratio', 'N/A'):.3f}" if isinstance(metrics.get('sharpe_ratio'), (int, float)) else "N/A")
        st.metric("Max Drawdown", f"{metrics.get('max_drawdown', 'N/A'):.2%}" if isinstance(metrics.get('max_drawdown'), (int, float)) else "N/A")
        
    with col2:
        st.metric("Volatility", f"{metrics.get('volatility', 'N/A'):.2%}" if isinstance(metrics.get('volatility'), (int, float)) else "N/A")
        st.metric("Beta", f"{metrics.get('beta', 'N/A'):.3f}" if isinstance(metrics.get('beta'), (int, float)) else "N/A")
        
    with col3:
        st.metric("VaR (95%)", f"{metrics.get('var_95', 'N/A'):.2%}" if isinstance(metrics.get('var_95'), (int, float)) else "N/A")
        st.metric("Alpha", f"{metrics.get('alpha', 'N/A'):.3f}" if isinstance(metrics.get('alpha'), (int, float)) else "N/A")
        
    with col4:
        st.metric("Total Return", f"{metrics.get('total_return', 'N/A'):.2%}" if isinstance(metrics.get('total_return'), (int, float)) else "N/A")
        st.metric("R²",