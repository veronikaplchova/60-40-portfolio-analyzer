"""Construct portfolios and perform market-regime analyses."""

import numpy as np
import pandas as pd

from config import (
    STOCK_TICKER,
    BOND_TICKER,
    STOCK_WEIGHT,
    BOND_WEIGHT,
    CORRELATION_WINDOW,
)


def construct_portfolio(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Construct monthly returns for a fixed-weight 60/40 portfolio."""

    portfolio_returns = returns.copy()
    portfolio_returns["60_40_portfolio"] = (
        STOCK_WEIGHT * portfolio_returns[STOCK_TICKER]
        + BOND_WEIGHT * portfolio_returns[BOND_TICKER]
    )

    return portfolio_returns


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
                "Annualized Volatility": (
                    regime_returns.std() * np.sqrt(12)
                ),
                "Negative Month Share": (regime_returns < 0).mean(),
            }
        )

    return pd.DataFrame(regime_results).set_index("Regime")


def calculate_rolling_correlations(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate stock-bond correlations using multiple rolling windows."""

    correlation_windows = [12, 36, 60]
    rolling_correlations = pd.DataFrame(index=returns.index)

    for window in correlation_windows:
        rolling_correlations[f"{window}-Month Correlation"] = (
            returns[STOCK_TICKER]
            .rolling(window=window)
            .corr(returns[BOND_TICKER])
        )

    return rolling_correlations


def analyze_crisis_periods(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Compare asset and portfolio performance during major crisis years."""

    crisis_periods = {
        "2008 Financial Crisis": ("2008-01-01", "2008-12-31"),
        "2020 COVID Crisis": ("2020-01-01", "2020-12-31"),
        "2022 Inflation Shock": ("2022-01-01", "2022-12-31"),
    }

    crisis_results = []

    for crisis_name, (start_date, end_date) in crisis_periods.items():
        crisis_returns = returns.loc[start_date:end_date]

        cumulative_values = (1 + crisis_returns).cumprod()
        previous_peaks = cumulative_values.cummax().clip(lower=1.0)
        portfolio_drawdowns = (
            cumulative_values["60_40_portfolio"]
            / previous_peaks["60_40_portfolio"]
            - 1
        )

        crisis_results.append(
            {
                "Crisis": crisis_name,
                "SPY Total Return": (
                    1 + crisis_returns[STOCK_TICKER]
                ).prod() - 1,
                "TLT Total Return": (
                    1 + crisis_returns[BOND_TICKER]
                ).prod() - 1,
                "60/40 Total Return": (
                    1 + crisis_returns["60_40_portfolio"]
                ).prod() - 1,
                "60/40 Volatility": (
                    crisis_returns["60_40_portfolio"].std()
                    * np.sqrt(12)
                ),
                "60/40 Maximum Drawdown": portfolio_drawdowns.min(),
                "Stock–Bond Correlation": crisis_returns[
                    STOCK_TICKER
                ].corr(crisis_returns[BOND_TICKER]),
            }
        )

    return pd.DataFrame(crisis_results).set_index("Crisis")