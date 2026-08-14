"""Analyze a traditional portfolio containing 60% stocks and 40% bonds."""

from config import (
    STOCK_TICKER,
    BOND_TICKER,
    START_DATE,
    END_DATE,
    
)

from data import (
    download_monthly_returns,
    download_monthly_risk_free_rate,
)

from metrics import (
    calculate_performance_metrics,
    calculate_maximum_drawdown,
    calculate_sharpe_ratios,
)

from analysis import (
    construct_portfolio,
    construct_allocation_portfolios,
    analyze_correlation_regimes,
    calculate_rolling_correlations,
    analyze_crisis_periods,
)

from plots import (
    plot_cumulative_growth,
    plot_rolling_correlation,
    plot_regime_comparison,
    plot_risk_return,
    plot_crisis_comparison,
    plot_correlation_robustness,
)















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
    rolling_correlations = calculate_rolling_correlations(results)

    rolling_correlations.to_csv(
      "results/rolling_correlation_robustness.csv"
)
    crisis_analysis = analyze_crisis_periods(results)

    crisis_analysis.to_csv(
      "results/crisis_comparison.csv"
)
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

    formatted_crises = crisis_analysis.copy()

    crisis_percentage_columns = [
        "SPY Total Return",
        "TLT Total Return",
        "60/40 Total Return",
        "60/40 Volatility",
        "60/40 Maximum Drawdown",
    ]

    for column in crisis_percentage_columns:
        formatted_crises[column] = formatted_crises[column].map(
            lambda value: f"{value:.2%}"
        )

    formatted_crises["Stock–Bond Correlation"] = formatted_crises[
        "Stock–Bond Correlation"
    ].map(lambda value: f"{value:.2f}")

    print("\nCrisis-period comparison:")
    print(formatted_crises)

    plot_cumulative_growth(results)
    plot_rolling_correlation(results)
    plot_correlation_robustness(rolling_correlations)
    plot_regime_comparison(regime_analysis)
    plot_crisis_comparison(crisis_analysis)
    plot_risk_return(allocation_performance)    

if __name__ == "__main__":
    main()