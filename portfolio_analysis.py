"""Analyze a traditional portfolio containing 60% stocks and 40% bonds."""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


STOCK_TICKER = "SPY"
BOND_TICKER = "TLT"
RISK_FREE_TICKER = "^IRX"
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

def analyze_correlation_regimes(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Compare 60/40 portfolio performance across correlation regimes."""

    rolling_correlation = (
        returns[STOCK_TICKER]
        .rolling(window=CORRELATION_WINDOW)
        .corr(returns[BOND_TICKER])
    )

    regime_data = pd.DataFrame(
        {
            "Portfolio Return": returns["60_40_portfolio"],
            "Correlation": rolling_correlation,
        }
    ).dropna()

    regime_results = []

    regimes = {
        "Negative correlation": regime_data["Correlation"] < 0,
        "Positive correlation": regime_data["Correlation"] >= 0,
    }

    for regime_name, condition in regimes.items():
        regime_returns = regime_data.loc[condition, "Portfolio Return"]

        regime_results.append(
            {
                "Regime": regime_name,
                "Months": len(regime_returns),
                "Annualized Average Return": regime_returns.mean() * 12,
                "Annualized Volatility": regime_returns.std() * np.sqrt(12),
                "Negative Month Share": (regime_returns < 0).mean(),
            }
        )

    return pd.DataFrame(regime_results).set_index("Regime")

def plot_regime_comparison(regime_analysis: pd.DataFrame) -> None:
    """Compare portfolio return and volatility across correlation regimes."""

    chart_data = regime_analysis[
        ["Annualized Average Return", "Annualized Volatility"]
    ] * 100

    ax = chart_data.plot(
        kind="bar",
        figsize=(10, 6),
        color=["steelblue", "darkorange"],
        width=0.7,
    )

    plt.title("60/40 Portfolio Performance by Correlation Regime")
    plt.xlabel("")
    plt.ylabel("Annualized percentage (%)")
    plt.xticks(rotation=0)
    plt.grid(axis="y", alpha=0.3)
    plt.legend(["Average Return", "Volatility"])

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f%%", padding=3)

    plt.tight_layout()
    plt.savefig(
        "results/figures/regime_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()

def construct_allocation_portfolios(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Construct portfolio returns for several stock-bond allocations."""

    allocations = {
        "100/0": (1.00, 0.00),
        "80/20": (0.80, 0.20),
        "60/40": (0.60, 0.40),
        "50/50": (0.50, 0.50),
        "40/60": (0.40, 0.60),
    }

    portfolio_returns = pd.DataFrame(index=returns.index)

    for portfolio_name, (stock_weight, bond_weight) in allocations.items():
        portfolio_returns[portfolio_name] = (
            stock_weight * returns[STOCK_TICKER]
            + bond_weight * returns[BOND_TICKER]
        )

    return portfolio_returns

def plot_risk_return(
    allocation_performance: pd.DataFrame,
) -> None:
    """Plot annualized return against volatility for each allocation."""

    volatility = allocation_performance["Annualized Volatility"] * 100
    annualized_return = allocation_performance["Annualized Return"] * 100

    plt.figure(figsize=(10, 6))
    plt.scatter(
        volatility,
        annualized_return,
        s=120,
        color="teal",
    )

    for allocation in allocation_performance.index:
        plt.annotate(
            allocation,
            (
                volatility.loc[allocation],
                annualized_return.loc[allocation],
            ),
            xytext=(7, 7),
            textcoords="offset points",
        )

    plt.title("Risk–Return Comparison of Stock–Bond Allocations")
    plt.xlabel("Annualized volatility (%)")
    plt.ylabel("Annualized return (%)")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "results/figures/risk_return_allocations.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


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

def calculate_sharpe_ratios(
    returns: pd.DataFrame,
    risk_free_rate: pd.Series,
) -> pd.Series:
    """Calculate annualized Sharpe ratios using monthly excess returns."""

    aligned_data = returns.join(risk_free_rate, how="inner")

    excess_returns = aligned_data[returns.columns].subtract(
        aligned_data["Risk-Free Rate"],
        axis=0,
    )

    sharpe_ratios = (
        excess_returns.mean()
        / excess_returns.std()
        * np.sqrt(12)
    )

    return sharpe_ratios


def main():
    """Run the portfolio analysis."""

    tickers = [STOCK_TICKER, BOND_TICKER]

    monthly_returns = download_monthly_returns(
        tickers,
        START_DATE,
        END_DATE,
    )

    risk_free_rate = download_monthly_risk_free_rate(
        START_DATE,
        END_DATE,
    )

    results = construct_portfolio(monthly_returns)
    allocation_returns = construct_allocation_portfolios(monthly_returns)
    allocation_performance = calculate_performance_metrics(allocation_returns)
    allocation_performance["Maximum Drawdown"] = (
        calculate_maximum_drawdown(allocation_returns)
    )
    allocation_performance["Sharpe Ratio"] = (
    calculate_sharpe_ratios(
        allocation_returns,
        risk_free_rate,
    )
)

    allocation_performance.to_csv(
        "results/allocation_comparison.csv"
    )
    performance = calculate_performance_metrics(results)

    maximum_drawdown = calculate_maximum_drawdown(results)
    performance["Maximum Drawdown"] = maximum_drawdown
    regime_analysis = analyze_correlation_regimes(results)
    regime_analysis.to_csv(
    "results/correlation_regime_comparison.csv"
)

    print("\nPerformance summary:")
    print(performance.map(lambda value: f"{value:.2%}"))

    formatted_allocations = allocation_performance.copy()

    allocation_percentage_columns = [
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
    ]

    for column in allocation_percentage_columns:
        formatted_allocations[column] = formatted_allocations[column].map(
            lambda value: f"{value:.2%}"
        )

    formatted_allocations["Sharpe Ratio"] = formatted_allocations[
        "Sharpe Ratio"
    ].map(lambda value: f"{value:.2f}")

    print("\nAllocation comparison:")
    print(formatted_allocations)

    formatted_regimes = regime_analysis.copy()

    regime_percentage_columns = [
        "Annualized Average Return",
        "Annualized Volatility",
        "Negative Month Share",
    ]

    for column in regime_percentage_columns:
        formatted_regimes[column] = formatted_regimes[column].map(
            lambda value: f"{value:.2%}"
        )

    print("\nCorrelation-regime comparison:")
    print(formatted_regimes)

    plot_cumulative_growth(results)
    plot_rolling_correlation(results)
    plot_regime_comparison(regime_analysis)
    plot_risk_return(allocation_performance)

if __name__ == "__main__":
    main()