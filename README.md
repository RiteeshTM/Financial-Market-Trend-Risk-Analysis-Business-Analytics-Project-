# 📈 Financial Market Trend & Risk Analysis

A comprehensive **Business Analytics** project that analyzes stock market data for major Indian equities — studying price trends, volatility, return distributions, and forecasting — powered by an interactive **Streamlit** dashboard.

---

## 🎯 Project Overview

This project performs an end-to-end financial analysis of **five major Indian stocks** listed on the NSE (National Stock Exchange), benchmarked against the **NIFTY 50** index. It covers:

- **Price Trend Analysis** — Historical closing price visualization and cumulative return tracking.
- **Risk Assessment** — Daily & annualized volatility, rolling volatility, Value at Risk (VaR), and maximum drawdown analysis.
- **Performance Metrics** — Annualized returns, Sharpe Ratio, and Beta (systematic risk vs. NIFTY 50).
- **Time-Series Forecasting** — ARIMA (1,0,1) model for short-term return predictions with stationarity testing (ADF test).
- **Return Distribution Analysis** — Log return distribution with KDE overlay for normality assessment.

### 📊 Stocks Analyzed

| Company       | NSE Ticker     |
|---------------|----------------|
| HDFC Bank     | `HDFCBANK.NS`  |
| Infosys       | `INFY.NS`      |
| ITC           | `ITC.NS`       |
| Reliance      | `RELIANCE.NS`  |
| TCS           | `TCS.NS`       |

---

## 🛠️ Tech Stack

| Technology     | Purpose                                      |
|----------------|----------------------------------------------|
| **Python**     | Core programming language                    |
| **Streamlit**  | Interactive web dashboard                    |
| **yfinance**   | Real-time & historical stock data from Yahoo Finance |
| **Pandas**     | Data manipulation & analysis                 |
| **NumPy**      | Numerical computations                       |
| **Matplotlib** | Static chart visualizations                  |
| **Seaborn**    | Statistical data visualizations              |
| **Statsmodels**| OLS regression (Beta), ADF test, ARIMA model |
| **Pytest**     | Unit & integration testing                   |

---

## 📁 Project Structure

```
Financial-Market-Trend-Risk-Analysis-Business-Analytics-Project-/
│
├── app.py                      # Streamlit dashboard application
├── infosys_code.py             # Standalone Infosys analysis script
├── requirements.txt            # Python dependencies
├── test_app.py                 # Unit & integration tests (pytest)
├── BA_report.pdf               # Business Analytics project report
│
├── HDFC_Analysis.ipynb         # Jupyter Notebook — HDFC Bank analysis
├── ITCAnalysis (2).ipynb       # Jupyter Notebook — ITC analysis
├── Reliance Analysis.ipynb     # Jupyter Notebook — Reliance analysis
├── TCS_Analysis .ipynb         # Jupyter Notebook — TCS analysis
├── infosys_analysis.ipynb      # Jupyter Notebook — Infosys analysis
│
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RiteeshTM/Financial-Market-Trend-Risk-Analysis-Business-Analytics-Project-.git
   cd Financial-Market-Trend-Risk-Analysis-Business-Analytics-Project-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit dashboard**
   ```bash
   streamlit run app.py
   ```

4. **Run the tests**
   ```bash
   pytest test_app.py -v
   ```

---

## 📊 Dashboard Features

The interactive Streamlit dashboard (`app.py`) provides:

### Sidebar Controls
- **Stock Selector** — Choose from HDFC Bank, Infosys, ITC, Reliance, or TCS.
- **Date Range Picker** — Customize the analysis period (default: Jan 2018 – present).
- **Risk-Free Rate Input** — Adjustable risk-free rate for Sharpe Ratio calculation (default: 7%).

### KPI Metrics Row
| Metric              | Description                                              |
|----------------------|----------------------------------------------------------|
| **Annual Return**    | Annualized log return (mean daily × 252)                 |
| **Annual Volatility**| Annualized standard deviation of log returns             |
| **Sharpe Ratio**     | Risk-adjusted return (excess return / volatility)        |
| **Beta (vs NIFTY)**  | Systematic risk via OLS regression against NIFTY 50      |
| **95% VaR (Daily)**  | 5th percentile of daily log returns (worst-case loss)    |

### Visualization Tabs

1. **Price History** — Stock closing price chart + cumulative returns growth curve.
2. **Risk & Returns** — 6-month rolling annualized volatility with average volatility baseline.
3. **Drawdown** — Maximum drawdown chart showing peak-to-trough declines.
4. **Distribution** — Histogram of log returns with KDE (Kernel Density Estimation) overlay.
5. **ARIMA Forecast** — Augmented Dickey-Fuller stationarity test + ARIMA(1,0,1) model summary + 5-day return forecast.

---

## 📓 Jupyter Notebook Analysis

Individual stock analyses are available as Jupyter Notebooks for detailed, step-by-step exploration:

- `HDFC_Analysis.ipynb` — HDFC Bank deep dive
- `ITCAnalysis (2).ipynb` — ITC deep dive
- `Reliance Analysis.ipynb` — Reliance Industries deep dive
- `TCS_Analysis .ipynb` — TCS deep dive
- `infosys_analysis.ipynb` — Infosys deep dive

Each notebook covers: data download, return calculations, volatility analysis, beta estimation, VaR, ARIMA forecasting, drawdown, and cumulative returns.

---

## 🧪 Testing

The project includes comprehensive tests in `test_app.py`:

- **`test_load_data()`** — Validates stock data loading, column creation (`simple_return`, `log_return`), and return calculations.
- **`test_load_market()`** — Validates NIFTY 50 market data loading and `market_return` column computation.
- **`test_streamlit_app_renders()`** — Full integration test using Streamlit's `AppTest` framework — verifies the dashboard renders without exceptions and displays all 5 KPI metrics.

Run tests with:
```bash
pytest test_app.py -v
```

---

## 📈 Key Financial Concepts Used

| Concept                  | Formula / Method                                                           |
|--------------------------|----------------------------------------------------------------------------|
| **Simple Return**        | `(Price_t - Price_{t-1}) / Price_{t-1}`                                    |
| **Log Return**           | `ln(Price_t / Price_{t-1})`                                                |
| **Annualized Volatility**| `Daily_Std × √252`                                                        |
| **Sharpe Ratio**         | `(Annual_Return - Risk_Free_Rate) / Annual_Volatility`                     |
| **Beta (CAPM)**          | OLS regression slope of stock returns vs. market (NIFTY 50) returns        |
| **Value at Risk (95%)**  | 5th percentile of daily log return distribution                            |
| **Maximum Drawdown**     | Largest peak-to-trough cumulative return decline                           |
| **ADF Test**             | Augmented Dickey-Fuller test for stationarity of return series              |
| **ARIMA(1,0,1)**         | AutoRegressive Integrated Moving Average model for return forecasting      |

---

## 📄 Report

A detailed Business Analytics report is available at **`BA_report.pdf`**, covering methodology, findings, and investment insights.

---

## ⚠️ Disclaimer

> The statistical data, calculations, and forecasts presented in this project are for **educational and analytical purposes only**. They do not constitute financial advice. Always consult a qualified financial advisor before making investment decisions.

---

## 📝 License

This project is open source and available for academic and personal use.
