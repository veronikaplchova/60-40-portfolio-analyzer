# 60/40 Portfolio Analyzer

A Python project analyzing stock–bond correlation and the historical performance of a traditional 60/40 portfolio.

## Project objective

This project investigates how changes in the relationship between stocks and bonds affect portfolio diversification.

The current analysis uses:

- SPY as a proxy for US stocks
- TLT as a proxy for long-term US Treasury bonds
- Monthly total returns from January 2005 through July 2026
- A portfolio containing 60% SPY and 40% TLT
- Monthly rebalancing

## Current features

- Downloads historical financial data
- Calculates monthly portfolio returns
- Calculates annualized return and volatility
- Calculates maximum drawdown
- Visualizes cumulative investment growth
- Estimates 36-month rolling stock–bond correlation

## Cumulative growth

![Cumulative growth of SPY, TLT, and the 60/40 portfolio](results/figures/cumulative_growth.png)

## Rolling stock–bond correlation

![36-month rolling correlation between SPY and TLT](results/figures/rolling_correlation.png)

## Correlation-regime comparison

The analysis compares 60/40 portfolio performance during periods of negative and positive 36-month stock–bond correlation.

![60/40 portfolio performance by correlation regime](results/figures/regime_comparison.png)

The portfolio produced a similar annualized mean return in both regimes. However, annualized volatility increased from 9.64% during negative-correlation periods to 13.67% during positive-correlation periods.

This descriptive result suggests that positive stock–bond correlation weakened the portfolio's diversification benefit by increasing risk without a corresponding increase in average return.

The comparison contains 173 negative-correlation months and 50 positive-correlation months. It describes historical associations and does not establish that positive correlation caused the difference in portfolio risk.

## Allocation comparison

The analyzer compares five stock–bond allocations ranging from 100% stocks to 40% stocks and 60% bonds.

![Risk–return comparison of stock–bond allocations](results/figures/risk_return_allocations.png)

Increasing the bond allocation generally reduced both historical return and volatility. The 60/40 portfolio achieved an annualized return of 8.19% with 10.05% volatility, compared with 10.97% return and 14.86% volatility for the stock-only portfolio.

The 50/50 allocation recorded the lowest volatility and smallest maximum drawdown in this sample. Increasing the bond weight to 60% did not reduce risk further, partly because long-duration Treasury bonds experienced substantial interest-rate risk.

These results describe SPY and TLT between January 2005 and July 2026 and do not identify one universally optimal allocation.

## Data source

Historical market data are downloaded through the `yfinance` Python package.

## Status

This project is under active development. Planned extensions include correlation-regime analysis, additional portfolio allocations, crisis-period comparisons, and an interactive dashboard.