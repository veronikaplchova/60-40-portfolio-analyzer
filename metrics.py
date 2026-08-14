"""Calculate portfolio performance and risk metrics."""

import numpy as np
import pandas as pd


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