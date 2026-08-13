"""Analyze a traditional portfolio containing 60% stocks and 40% bonds."""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


STOCK_TICKER = "SPY"
BOND_TICKER = "TLT"
START_DATE = "2005-01-01"
END_DATE = "2026-08-01"

STOCK_WEIGHT = 0.60
BOND_WEIGHT = 0.40
CORRELATION_WINDOW = 36


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


def construct_portfolio(returns):
    """Construct monthly returns for a fixed-weight 60/40 portfolio."""

    portfolio_returns = returns.copy()
    portfolio_returns["60_40_portfolio"] = (
        STOCK_WEIGHT * portfolio_returns[STOCK_TICKER]
        + BOND_WEIGHT * portfolio_returns[BOND_TICKER]
    )
    return portfolio_returns

def calculate_performance_metrics(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate annualized return and volatility for each investment."""

    months = len(returns)

    annualized_return = (
        (1 + returns).prod() ** (12 / months) - 1
    )
    annualized_volatility = returns.std() * np.sqrt(12)

    return pd.DataFrame(
        {
            "Annualized Return": annualized_return,
            "Annualized Volatility": annualized_volatility,
        }
    )



def calculate_maximum_drawdown(
    returns: pd.DataFrame,
) -> pd.Series:
    """Calculate the largest peak-to-trough loss for each investment."""

    cumulative_value = (1 + returns).cumprod()
    previous_peaks = cumulative_value.cummax()
    drawdowns = cumulative_value / previous_peaks - 1

    return drawdowns.min()


def plot_cumulative_growth(returns: pd.DataFrame) -> None:
    """Plot the growth of one dollar invested in each asset."""

    cumulative_growth = (1 + returns).cumprod()

    cumulative_growth.plot(
        figsize=(11, 6),
        linewidth=2,
    )

    plt.title("Growth of $1 Invested: SPY, TLT, and 60/40 Portfolio")
    plt.xlabel("Date")
    plt.ylabel("Portfolio value ($)")
    plt.grid(alpha=0.3)
    plt.legend(["SPY (Stocks)", "TLT (Bonds)", "60/40 Portfolio"])
    plt.tight_layout()
    plt.savefig(
    "results/figures/cumulative_growth.png",
    dpi=300,
    bbox_inches="tight",
)
    plt.show()

def plot_rolling_correlation(returns: pd.DataFrame) -> None:
    """Plot the rolling correlation between stock and bond returns."""

    rolling_correlation = (
        returns[STOCK_TICKER]
        .rolling(window=CORRELATION_WINDOW)
        .corr(returns[BOND_TICKER])
    )

    plt.figure(figsize=(11, 6))
    plt.plot(
        rolling_correlation.index,
        rolling_correlation,
        color="purple",
        linewidth=2,
    )
    plt.axhline(0, color="black", linewidth=1, linestyle="--")

    plt.title(
        f"{CORRELATION_WINDOW}-Month Rolling Correlation: "
        f"{STOCK_TICKER} and {BOND_TICKER}"
    )
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.ylim(-1, 1)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "results/figures/rolling_correlation.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def main():
    """Run the portfolio analysis."""

    tickers = [STOCK_TICKER, BOND_TICKER]

    monthly_returns = download_monthly_returns(
        tickers,
        START_DATE,
        END_DATE,
    )

    results = construct_portfolio(monthly_returns)
    performance = calculate_performance_metrics(results)

    maximum_drawdown = calculate_maximum_drawdown(results)
    performance["Maximum Drawdown"] = maximum_drawdown

    print("\nPerformance summary:")
    print(performance.map(lambda value: f"{value:.2%}"))
    plot_cumulative_growth(results)
    plot_rolling_correlation(results)

if __name__ == "__main__":
    main()