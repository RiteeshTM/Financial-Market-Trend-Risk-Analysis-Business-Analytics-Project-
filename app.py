import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import datetime
st.set_page_config(page_title="Indian Equities Dashboard", layout="wide", page_icon="📈")

# High-Contrast Chart Styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'text.color': '#1e293b',
    'axes.labelcolor': '#1e293b',
    'xtick.color': '#475569',
    'ytick.color': '#475569',
    'axes.titlecolor': '#0f172a',
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'grid.color': '#e2e8f0'
})

# Custom CSS for Premium, Responsive UI
st.markdown("""
<style>
    /* Theme Variables */
    :root {
        --header-bg: #1e293b;
        --header-border: rgba(255, 255, 255, 0.2);
        --header-text: #ffffff;
        --subtitle-text: #94a3b8;
        --metric-val: #3b82f6;  /* Blue accents for dark mode */
        --metric-label: #94a3b8;
    }

    @media (prefers-color-scheme: light) {
        :root {
            --header-bg: #f1f5f9;
            --header-border: #cbd5e1;
            --header-text: #0f172a;
            --subtitle-text: #334155;
            --metric-val: #1e3a8a !important; /* High contrast dark blue */
            --metric-label: #0f172a !important; /* Pure dark for visibility */
        }
    }

    .main-header {
        background-color: var(--header-bg) !important;
        border: 2px solid var(--header-border) !important;
        padding: 1.5rem;
        border-radius: 12px;
        color: var(--header-text) !important;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1.2s ease;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: var(--header-text) !important;
    }
    
    .header-subtitle {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--subtitle-text) !important;
        opacity: 1 !important;
    }

    /* FORCING HIGH CONTRAST ON METRICS */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: var(--metric-val) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700 !important;
        color: var(--metric-label) !important;
        opacity: 1 !important;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: var(--header-bg) !important;
        border-radius: 8px 8px 0px 0px;
        color: var(--header-text) !important;
        padding: 0 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Refined Header Setup
st.markdown("""
    <div class="main-header">
        <div class="header-title">📈 Indian Equities Analytics</div>
        <div class="header-subtitle">Advanced Financial Trend & Risk Analysis Dashboard</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("Configuration")
stocks_dict = {
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ITC": "ITC.NS",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS"
}

selected_stock = st.sidebar.selectbox("Select Stock", list(stocks_dict.keys()))
ticker = stocks_dict[selected_stock]

start_date = st.sidebar.date_input("Start Date", datetime.date(2018, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (Annual)", value=0.07, step=0.01)

# Function to fetch data
@st.cache_data
def load_data(ticker_symbol, start, end):
    data = yf.download(ticker_symbol, start=start, end=end, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns.name = None
    
    # Calculate returns
    data["simple_return"] = data["Close"].pct_change()
    data["log_return"] = np.log(data["Close"] / data["Close"].shift(1))
    
    return data.dropna()

@st.cache_data
def load_market(start, end):
    market = yf.download("^NSEI", start=start, end=end, auto_adjust=True)
    if isinstance(market.columns, pd.MultiIndex):
        market.columns = market.columns.get_level_values(0)
    market.columns.name = None
    market["market_return"] = np.log(market["Close"] / market["Close"].shift(1))
    return market.dropna()

data_load_state = st.text('Loading data...')
try:
    data = load_data(ticker, start_date, end_date)
    market = load_market(start_date, end_date)
    data_load_state.text('Data loaded successfully!')
    st.sidebar.success("Data loaded successfully!")
except Exception as e:
    data_load_state.text(f"Error loading data: {e}")
    st.stop()
    
# Layout Metrics
# Core Calculations
daily_volatility = data["log_return"].std()
annual_volatility = daily_volatility * np.sqrt(252)
annual_return = data["log_return"].mean() * 252
sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
VaR_95 = np.percentile(data["log_return"], 5)

# Beta Calculation
df_beta = pd.concat([data["log_return"], market["market_return"]], axis=1).dropna()
X = sm.add_constant(df_beta["market_return"])
y = df_beta["log_return"]
model = sm.OLS(y, X).fit()
beta = model.params["market_return"]

# Display KPI Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Annual Return", f"{annual_return:.2%}")
with col2:
    st.metric("Annual Volatility", f"{annual_volatility:.2%}")
with col3:
    st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
with col4:
    st.metric("Beta (vs NIFTY)", f"{beta:.2f}")
with col5:
    st.metric("95% VaR (Daily)", f"{VaR_95:.2%}")

# Tabs for visualisations
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Price History", "Risk & Returns", "Drawdown", "Distribution", "ARIMA Forecast"])

with tab1:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data.index, data["Close"])
    ax.set_title(f"{selected_stock} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    st.pyplot(fig)
    
    st.subheader("Cumulative Returns")
    cum_returns = (1 + data["simple_return"]).cumprod()
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(cum_returns.index, cum_returns)
    ax2.set_title(f"Cumulative Returns ({selected_stock})")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Growth of $1 Investment")
    st.pyplot(fig2)

with tab2:
    rolling_vol = data["log_return"].rolling(window=126).std() * np.sqrt(252)
    avg_vol = data["log_return"].std() * np.sqrt(252)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(rolling_vol.index, rolling_vol, color='#dd8452', linewidth=2, label='Volatility')
    ax.axhline(y=avg_vol, color='#4c72b0', linestyle='--', linewidth=2, label='Average volatility')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1)
    ax.set_title("Rolling volatility (6-month)")
    ax.set_xlabel("")
    ax.set_ylabel("Volatility")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

with tab3:
    cum_returns = (1 + data["simple_return"]).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = cum_returns / rolling_max - 1
    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(drawdown.index, drawdown)
    ax.set_title(f"Maximum Drawdown ({selected_stock})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    st.pyplot(fig)

with tab4:
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(data["log_return"], bins=50, kde=True, ax=ax)
    ax.set_title("Distribution of Log Returns")
    st.pyplot(fig)

with tab5:
    st.subheader("ARIMA (1,0,1) 5-Day Forecast")
    
    try:
        # Check stationarity
        result = adfuller(data["log_return"].dropna())
        st.write(f"**ADF Statistic:** {result[0]:.4f} | **p-value:** {result[1]:.4e}")
        st.write("*(p-value < 0.05 implies stationary returns)*")
        
        with st.spinner("Fitting ARIMA Model..."):
            arima_model = ARIMA(data["log_return"], order=(1,0,1))
            model_fit = arima_model.fit()
            st.text("ARIMA Model Summary:")
            st.text(model_fit.summary().as_text())
            
            forecast = model_fit.forecast(steps=5)
            st.write("**Next 5 day forecast of log returns:**")
            st.dataframe(forecast, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error computing ARIMA: {str(e)}")

st.markdown("---")
st.markdown("*Disclaimer: The statistical data and calculations are for analytical purposes only, not financial advice.*")
