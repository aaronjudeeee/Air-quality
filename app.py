import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

API_KEY = "your_alpha_vantage_api_key"  # Replace with your Alpha Vantage API key

st.title("📈 Real-Time Stock Market Dashboard")

ticker = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT):", "AAPL").upper()

def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Error Message" in data:
        return None, "Invalid symbol or API limit reached."
    if "Time Series (Daily)" not in data:
        return None, "Unexpected API response."

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. adjusted close": "Adj Close",
        "6. volume": "Volume",
        "7. dividend amount": "Dividend",
        "8. split coefficient": "Split Coeff"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.astype(float)
    return df, None

if ticker:
    with st.spinner(f"Fetching data for {ticker}..."):
        df, error = fetch_stock_data(ticker)
    if error:
        st.error(error)
    else:
        st.subheader(f"Stock Prices for {ticker}")
        st.write(df.tail(10))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name='Close Price'))
        fig.update_layout(title=f"{ticker} Closing Prices",
                          xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)

        latest_close = df["Close"].iloc[-1]
        previous_close = df["Close"].iloc[-2]
        change = latest_close - previous_close
        change_pct = (change / previous_close) * 100
        st.metric(label="Latest Close Price", value=f"${latest_close:.2f}", delta=f"{change_pct:.2f}%")





