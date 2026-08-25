"""Interactive dashboard for the 60/40 portfolio analysis."""

from datetime import date

import pandas as pd
import streamlit as st

from config import STOCK_TICKER, BOND_TICKER
from data import download_monthly_returns
from metrics import (
    calculate_performance_metrics,
    calculate_maximum_drawdown,
)


st.set_page_config(
    page_title="60/40 Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
)


@st.cache_data(ttl=3600)
def load_market_data(
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Download and temporarily cache monthly market returns."""

    return download_monthly_returns(
        [STOCK_TICKER, BOND_TICKER],
        start_date,
        end_date,
    )


st.title("Interactive 60/40 Portfolio Analyzer")

st.write(
    "Explore how portfolio weights, dates, and the correlation window "
    "affect historical stock–bond diversification."
)

st.sidebar.header("Portfolio settings")

stock_weight_percent = st.sidebar.slider(
    "Stock weight (%)",
    min_value=0,
    max_value=100,
    value=60,
    step=5,
)

bond_weight_percent = 100 - stock_weight_percent

st.sidebar.write(f"Bond weight: **{bond_weight_percent}%**")

start_date = st.sidebar.date_input(
    "Start date",
    value=date(2005, 1, 1),
)

end_date = st.sidebar.date_input(
    "End date",
    value=date.today(),
)

correlation_window = st.sidebar.select_slider(
    "Rolling-correlation window",
    options=[12, 36, 60],
    value=36,
    format_func=lambda value: f"{value} months",
)

if start_date >= end_date:
    st.error("The end date must be later than the start date.")
    st.stop()

with st.spinner("Downloading market data..."):
    returns = load_market_data(
        start_date.isoformat(),
        end_date.isoformat(),
    )

if returns.empty:
    st.error(
        "No market data were downloaded. Please try different dates "
        "or refresh the dashboard."
    )
    st.stop()

stock_weight = stock_weight_percent / 100
bond_weight = bond_weight_percent / 100

portfolio_name = (
    f"{stock_weight_percent}/{bond_weight_percent} Portfolio"
)

returns[portfolio_name] = (
    stock_weight * returns[STOCK_TICKER]
    + bond_weight * returns[BOND_TICKER]
)

performance = calculate_performance_metrics(
    returns[[portfolio_name]]
)

maximum_drawdown = calculate_maximum_drawdown(
    returns[[portfolio_name]]
).loc[portfolio_name]

rolling_correlation = (
    returns[STOCK_TICKER]
    .rolling(window=correlation_window)
    .corr(returns[BOND_TICKER])
)

valid_correlations = rolling_correlation.dropna()

if valid_correlations.empty:
    latest_correlation = None
else:
    latest_correlation = valid_correlations.iloc[-1]

st.subheader("Portfolio performance")

return_column, volatility_column = st.columns(2)
drawdown_column, correlation_column = st.columns(2)

return_column.metric(
    "Annualized return",
    f"{performance.loc[portfolio_name, 'Annualized Return']:.2%}",
)

volatility_column.metric(
    "Annualized volatility",
    f"{performance.loc[portfolio_name, 'Annualized Volatility']:.2%}",
)

drawdown_column.metric(
    "Maximum drawdown",
    f"{maximum_drawdown:.2%}",
)

correlation_column.metric(
    "Latest correlation",
    (
        f"{latest_correlation:.2f}"
        if latest_correlation is not None
        else "Not enough data"
    ),
)

st.subheader("Cumulative growth of $1")

cumulative_growth = (
    1 + returns[[STOCK_TICKER, BOND_TICKER, portfolio_name]]
).cumprod()

cumulative_growth = cumulative_growth.rename(
    columns={
        STOCK_TICKER: "SPY (Stocks)",
        BOND_TICKER: "TLT (Bonds)",
    }
)

st.line_chart(cumulative_growth)

st.subheader(
    f"{correlation_window}-month rolling stock–bond correlation"
)

correlation_chart = rolling_correlation.rename(
    "Stock–Bond Correlation"
).to_frame()

st.line_chart(correlation_chart)

st.caption(
    "Historical results are descriptive and exclude fees, taxes, "
    "transaction costs, and inflation."
)