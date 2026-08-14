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

- Downloads adjusted historical prices through `yfinance`
- Converts daily prices into monthly total returns
- Constructs a monthly rebalanced 60/40 portfolio
- Calculates annualized return, volatility, maximum drawdown, and Sharpe ratios
- Compares five stock–bond allocations
- Estimates 12-, 36-, and 60-month rolling stock–bond correlations
- Compares portfolio performance across negative- and positive-correlation regimes
- Examines performance during the 2008, 2020, and 2022 crisis years
- Exports result tables to CSV
- Creates and saves six analytical charts
- Organizes data, calculations, analysis, and plotting into separate Python modules

## Methodology

Adjusted closing prices for SPY and TLT are converted into month-end total returns. The baseline portfolio allocates 60% to SPY and 40% to TLT and is rebalanced monthly.

Performance is evaluated using annualized return, annualized volatility, maximum drawdown, and the Sharpe ratio. Sharpe ratios use the 13-week US Treasury bill yield (`^IRX`) as the risk-free-rate proxy.

Diversification is examined using a 36-month rolling stock–bond correlation. Portfolio performance is then compared between negative- and positive-correlation regimes. Robustness is assessed using alternative 12- and 60-month windows.

The crisis analysis uses the full calendar years 2008, 2020, and 2022 to ensure that returns are measured over consistent periods. All results are descriptive and based on historical associations.

## Key findings

- The 60/40 portfolio returned 8.19% annually with 10.05% annualized volatility over the sample.
- Portfolio volatility increased from 9.64% during negative-correlation periods to 13.67% during positive-correlation periods, while average returns remained similar.
- The transition toward positive stock–bond correlation around 2022–2023 appears across 12-, 36-, and 60-month windows.
- Bonds substantially cushioned stock losses in 2008, but both assets declined in 2022, causing the 60/40 portfolio to lose 23.31%.
- The 80/20 allocation recorded the highest historical Sharpe ratio among the five tested portfolios, while the 50/50 allocation recorded the lowest volatility.

## Cumulative growth

![Cumulative growth of SPY, TLT, and the 60/40 portfolio](results/figures/cumulative_growth.png)

## Rolling stock–bond correlation

![36-month rolling correlation between SPY and TLT](results/figures/rolling_correlation.png)

## Robustness checks

To test whether the observed correlation pattern depends on the selected window length, the analysis compares 12-, 36-, and 60-month rolling correlations.

![Robustness check using alternative rolling-correlation windows](results/figures/correlation_robustness.png)

The 12-month correlation is more responsive to recent market movements but is also considerably more volatile. The 60-month correlation changes more gradually and represents a longer-term relationship, while the 36-month measure provides an intermediate specification.

Despite these differences, all three windows identify a broad transition from predominantly negative stock–bond correlation to positive correlation around 2022–2023. This indicates that the main conclusion is not driven solely by the choice of a 36-month rolling window.

## Correlation-regime comparison

The analysis compares 60/40 portfolio performance during periods of negative and positive 36-month stock–bond correlation.

![60/40 portfolio performance by correlation regime](results/figures/regime_comparison.png)

The portfolio produced a similar annualized mean return in both regimes. However, annualized volatility increased from 9.64% during negative-correlation periods to 13.67% during positive-correlation periods.

This descriptive result suggests that positive stock–bond correlation weakened the portfolio's diversification benefit by increasing risk without a corresponding increase in average return.

The comparison contains 173 negative-correlation months and 50 positive-correlation months. It describes historical associations and does not establish that positive correlation caused the difference in portfolio risk.

## Crisis-period comparison

The analysis compares SPY, TLT, and the 60/40 portfolio during the 2008 financial crisis, the 2020 COVID crisis, and the 2022 inflation shock.

![Asset and 60/40 portfolio performance during crisis years](results/figures/crisis_comparison.png)

During 2008, SPY lost 36.80%, while TLT gained 33.95%. The opposing bond performance cushioned the portfolio, limiting the 60/40 loss to 13.36%.

In 2020, SPY and TLT both finished the full calendar year positively, and the 60/40 portfolio returned 19.80%. These annual results include the strong market recovery that followed the initial COVID crash.

The outcome was substantially different in 2022. SPY lost 18.18%, TLT lost 31.23%, and the 60/40 portfolio lost 23.31%. Stock–bond correlation was positive at 0.51, meaning that bonds did not provide their traditional protection when stocks declined.

These episodes illustrate that the effectiveness of a 60/40 portfolio depends not only on the performance of each asset but also on how stocks and bonds move relative to one another.

## Allocation comparison

The analyzer compares five stock–bond allocations ranging from 100% stocks to 40% stocks and 60% bonds.


![Risk–return comparison of stock–bond allocations](results/figures/risk_return_allocations.png)

Increasing the bond allocation generally reduced both historical return and volatility. The 60/40 portfolio achieved an annualized return of 8.19% with 10.05% volatility, compared with 10.97% return and 14.86% volatility for the stock-only portfolio.

The 50/50 allocation recorded the lowest volatility and smallest maximum drawdown in this sample. Increasing the bond weight to 60% did not reduce risk further, partly because long-duration Treasury bonds experienced substantial interest-rate risk.

The 80/20 allocation recorded the highest Sharpe ratio at 0.69, indicating the strongest historical excess return per unit of volatility among the tested portfolios. The 60/40 portfolio and the stock-only portfolio both recorded Sharpe ratios of approximately 0.66, although the 60/40 portfolio experienced substantially lower volatility and a smaller maximum drawdown.

Sharpe ratios are calculated from monthly excess returns using the 13-week US Treasury bill yield (`^IRX`) as the risk-free-rate proxy. These historical results depend on the selected assets, sample period, rebalancing assumption, and the use of volatility as the measure of risk.

These results describe SPY and TLT between January 2005 and July 2026 and do not identify one universally optimal allocation.

## Limitations

- SPY and TLT represent only US equities and long-duration US Treasury bonds, so the findings may not apply to other markets or bond maturities.
- The analysis begins in 2005 because of TLT data availability and therefore does not cover earlier inflation and interest-rate regimes.
- The portfolio assumes fixed monthly rebalancing and excludes transaction costs, taxes, management fees, and bid–ask spreads.
- Crisis periods are measured using full calendar years, which can conceal substantial movements within each year, particularly the 2020 crash and recovery.
- Rolling correlations depend on the selected assets, sample period, data frequency, and window length.
- Historical relationships do not establish causality and do not guarantee future portfolio performance.


## Installation and usage

Clone the repository and open the project folder:

```bash
git clone https://github.com/veronikaplchova/60-40-portfolio-analyzer.git
cd 60-40-portfolio-analyzer
```

Install the required Python packages:

```bash
python3 -m pip install -r requirements.txt
```

Run the complete analysis:

```bash
python3 portfolio_analysis.py
```

The script downloads updated market data, prints performance tables in the terminal, and saves CSV results and charts in the `results` folder.

An internet connection is required because the market data are downloaded through Yahoo Finance.


## Project structure

The project is divided into focused Python modules:

- `config.py` defines tickers, portfolio weights, dates, and the main correlation window.
- `data.py` downloads market data and prepares monthly returns and risk-free rates.
- `metrics.py` calculates annualized performance, volatility, maximum drawdown, and Sharpe ratios.
- `analysis.py` constructs portfolios and performs correlation-regime, crisis-period, and robustness analyses.
- `plots.py` creates and saves all visualizations.
- `portfolio_analysis.py` coordinates the full analytical workflow.

## Data source

Historical market data are downloaded through the `yfinance` Python package.

## Status

The core analysis is complete. Potential future extensions include an interactive dashboard, additional asset classes, and alternative equity and bond proxies.