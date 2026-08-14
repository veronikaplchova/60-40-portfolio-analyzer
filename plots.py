"""Create and save charts for the portfolio analysis."""

import matplotlib.pyplot as plt
import pandas as pd

from config import (
    STOCK_TICKER,
    BOND_TICKER,
    CORRELATION_WINDOW,
)


def plot_cumulative_growth(returns: pd.DataFrame) -> None:
    """Plot the growth of one dollar invested in each asset."""

    cumulative_growth = (1 + returns).cumprod()

    cumulative_growth.plot(figsize=(11, 6), linewidth=2)

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


def plot_regime_comparison(
    regime_analysis: pd.DataFrame,
) -> None:
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


def plot_crisis_comparison(
    crisis_analysis: pd.DataFrame,
) -> None:
    """Plot asset and portfolio returns during major crisis years."""

    chart_data = crisis_analysis[
        [
            "SPY Total Return",
            "TLT Total Return",
            "60/40 Total Return",
        ]
    ] * 100

    ax = chart_data.plot(
        kind="bar",
        figsize=(11, 6),
        color=["steelblue", "darkorange", "seagreen"],
        width=0.75,
    )

    plt.title("Asset and 60/40 Portfolio Performance During Crisis Years")
    plt.xlabel("")
    plt.ylabel("Total return (%)")
    plt.xticks(rotation=0)
    plt.grid(axis="y", alpha=0.3)
    plt.legend(["SPY (Stocks)", "TLT (Bonds)", "60/40 Portfolio"])
    plt.axhline(0, color="black", linewidth=1)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)

    plt.tight_layout()
    plt.savefig(
        "results/figures/crisis_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def plot_correlation_robustness(
    rolling_correlations: pd.DataFrame,
) -> None:
    """Compare rolling correlations across different window lengths."""

    plt.figure(figsize=(12, 7))

    plt.plot(
        rolling_correlations.index,
        rolling_correlations["12-Month Correlation"],
        label="12-month window",
        color="lightcoral",
        linewidth=1.5,
        alpha=0.8,
    )
    plt.plot(
        rolling_correlations.index,
        rolling_correlations["36-Month Correlation"],
        label="36-month window",
        color="purple",
        linewidth=2.5,
    )
    plt.plot(
        rolling_correlations.index,
        rolling_correlations["60-Month Correlation"],
        label="60-month window",
        color="teal",
        linewidth=2,
    )

    plt.axhline(0, color="black", linewidth=1, linestyle="--")
    plt.title("Robustness Check: Stock–Bond Rolling Correlation")
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.ylim(-1, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        "results/figures/correlation_robustness.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()