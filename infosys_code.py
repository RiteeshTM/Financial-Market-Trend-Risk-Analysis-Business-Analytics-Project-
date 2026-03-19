import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

data = yf.download("INFY.NS", start="2018-01-01", auto_adjust=True)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
data.columns.name = None
data.tail()

data["simple_return"] = data["Close"].pct_change()

data["log_return"] = np.log(data["Close"] / data["Close"].shift(1))

data = data.dropna()

data

plt.figure(figsize=(10,5))
plt.plot(data.index, data["Close"])
plt.title("Infosys Stock Price")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

daily_volatility = data["log_return"].std()

annual_volatility = daily_volatility * np.sqrt(252)

print("Daily Volatility:", daily_volatility)
print("Annual Volatility:", annual_volatility)

annual_return = data["log_return"].mean() * 252

risk_free_rate = 0.07

sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility

print("Annual Return:", annual_return)
print("Sharpe Ratio:", sharpe_ratio)

# Download NIFTY market data
market = yf.download("^NSEI", start="2018-01-01", auto_adjust=True)

# Fix column structure if needed
if isinstance(market.columns, pd.MultiIndex):
    market.columns = market.columns.get_level_values(0)

# Calculate market returns
market["market_return"] = np.log(
    market["Close"] / market["Close"].shift(1)
)

# Merge Infosys and market returns
df = pd.concat([data["log_return"], market["market_return"]], axis=1).dropna()

# Regression
X = sm.add_constant(df["market_return"])
y = df["log_return"]

model = sm.OLS(y, X).fit()

# Get Beta (correct way)
beta = model.params["market_return"]

print("Beta:", beta)

VaR_95 = np.percentile(data["log_return"], 5)

print("95% Value at Risk:", VaR_95)

result = adfuller(data["log_return"])

print("ADF Statistic:", result[0])
print("p-value:", result[1])

model = ARIMA(data["log_return"], order=(1,0,1))

model_fit = model.fit()

print(model_fit.summary())

forecast = model_fit.forecast(steps=5)

print("Next 5 day forecast:")

print(forecast)

plt.figure(figsize=(8,5))

sns.histplot(data["log_return"], bins=50, kde=True)

plt.title("Distribution of Log Returns")

plt.show()

!pip install pyfolio-reloaded

import pyfolio as pf
import pandas as pd
import numpy as np
import yfinance as yf

market = yf.download("^NSEI", start="2018-01-01", auto_adjust=True)

# fix multiindex if present
if isinstance(market.columns, pd.MultiIndex):
    market.columns = market.columns.get_level_values(0)

# display market table
market.tail()

market["market_return"] = np.log(
    market["Close"] / market["Close"].shift(1)
)

benchmark_returns = market["market_return"].dropna()

benchmark_returns.head()

import pyfolio as pf
import pandas as pd
import numpy as np
import yfinance as yf

# Redefine data (from cell Mu8ZsVI1j348 and eO1lNPdekIdF)
data = yf.download("INFY.NS", start="2018-01-01", auto_adjust=True)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
data.columns.name = None
data["simple_return"] = data["Close"].pct_change()
data["log_return"] = np.log(data["Close"] / data["Close"].shift(1))
data = data.dropna()

# Redefine market (from cell J1MJ0emFl-eK)
market = yf.download("^NSEI", start="2018-01-01", auto_adjust=True)
if isinstance(market.columns, pd.MultiIndex):
    market.columns = market.columns.get_level_values(0)
market["market_return"] = np.log(
    market["Close"] / market["Close"].shift(1)
)

# Re-define returns and benchmark_returns for robustness
returns = data["log_return"]
benchmark_returns = market["market_return"].dropna()

# Localize indices
returns.index = returns.index.tz_localize(None)
benchmark_returns.index = benchmark_returns.index.tz_localize(None)

pf.create_returns_tear_sheet(
    returns,
    benchmark_rets=benchmark_returns
)


pf.plotting.plot_rolling_volatility(returns)

pf.plotting.plot_rolling_sharpe(returns)

pf.plotting.plot_drawdown_periods(returns)

data["rolling_vol"] = data["log_return"].rolling(30).std()

plt.figure(figsize=(10,5))
plt.plot(data["rolling_vol"])
plt.title("30-Day Rolling Volatility (Infosys)")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.show()

# Maximum Drawdown

cum_returns = (1 + data["simple_return"]).cumprod()

rolling_max = cum_returns.cummax()

drawdown = cum_returns / rolling_max - 1

plt.figure(figsize=(10,5))
plt.plot(drawdown)
plt.title("Maximum Drawdown (Infosys)")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.show()

# Cumulative Returns

cum_returns = (1 + data["simple_return"]).cumprod()

plt.figure(figsize=(10,5))
plt.plot(cum_returns)
plt.title("Cumulative Returns (Infosys)")
plt.xlabel("Date")
plt.ylabel("Growth of $1 Investment")
plt.show()



