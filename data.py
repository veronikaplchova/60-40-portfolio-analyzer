"""Download and prepare financial market data."""

import pandas as pd
import yfinance as yf

from config import RISK_FREE_TICKER


def download_monthly_returns(
    tickers: list[str],
    start_date: str,
    end_date: str,
):
    """Download market prices and convert them into monthly returns."""

    daily_prices = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )["Close"]

    monthly_prices = daily_prices.resample("ME").last()
    return monthly_prices.pct_change().dropna()


def download_monthly_risk_free_rate(
    start_date: str,
    end_date: str,
) -> pd.Series:
    """Download Treasury bill yields and convert them to monthly returns."""

    daily_yield = yf.download(
        RISK_FREE_TICKER,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )["Close"].squeeze()

    monthly_yield = daily_yield.resample("ME").last()

    monthly_risk_free_rate = (
        (1 + monthly_yield / 100) ** (1 / 12) - 1
    )

    return monthly_risk_free_rate.rename("Risk-Free Rate")