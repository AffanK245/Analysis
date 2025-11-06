import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Stock Market Analyzer", layout="wide")

st.title("📈 Stock Market Analyzer")
st.write("Enter a stock symbol (like AAPL, TSLA, MSFT) to view price trends and analysis.")

# --- User input ---
symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=1)
interval = st.selectbox("Select Interval", ["1d", "1h", "30m"], index=0)

if st.button("Analyze Stock"):
    try:
        st.info(f"Fetching data for **{symbol}**...")
        data = yf.download(symbol, period=period, interval=interval)

        if data.empty:
            st.error("No data found! Try a valid stock symbol.")
        else:
            # --- Data analysis ---
            data["Daily Change %"] = data["Close"].pct_change() * 100
            data["MA5"] = data["Close"].rolling(window=5).mean()
            data["MA20"] = data["Close"].rolling(window=20).mean()

            # --- Display data summary ---
            st.subheader("📊 Stock Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Close", f"${data['Close'].mean():.2f}")
            col2.metric("Highest Close", f"${data['Close'].max():.2f}")
            col3.metric("Lowest Close", f"${data['Close'].min():.2f}")

            # --- Plotting ---
            st.subheader("📈 Price Trend with Moving Averages")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data.index, data["Close"], label="Close Price", linewidth=1.5)
            ax.plot(data.index, data["MA5"], label="MA 5", linestyle="--")
            ax.plot(data.index, data["MA20"], label="MA 20", linestyle="--")
            ax.set_title(f"{symbol} Stock Price Trend")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            # --- Show raw data ---
            with st.expander("Show Raw Data"):
                st.dataframe(data.tail(20))

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
