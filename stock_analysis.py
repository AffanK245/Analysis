import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys

def analyze_stock(symbol="AAPL"):
    print(f"Fetching stock data for {symbol}...")
    # Download last 3 months of data
    data = yf.download(symbol, period="3mo", interval="1d")

    if data.empty:
        print("No data found for the symbol.")
        sys.exit(2)

    # Calculate technical indicators
    data["Daily Change %"] = data["Close"].pct_change() * 100
    data["MA5"] = data["Close"].rolling(window=5).mean()
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["Volatility"] = data["Daily Change %"].rolling(window=10).std()

    # Print summary statistics
    print("\n--- Stock Summary ---")
    print(f"Symbol: {symbol}")
    print(f"Start Date: {data.index.min().date()}")
    print(f"End Date: {data.index.max().date()}")
    print(f"Average Close Price: {data['Close'].mean():.2f}")
    print(f"Highest Close Price: {data['Close'].max():.2f}")
    print(f"Lowest Close Price: {data['Close'].min():.2f}")
    print(f"Average Volatility (10-day): {data['Volatility'].mean():.2f}%")

    # Plot close price and moving averages
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["Close"], label="Close Price", linewidth=1.5)
    plt.plot(data.index, data["MA5"], label="5-day MA")
    plt.plot(data.index, data["MA20"], label="20-day MA")
    plt.title(f"{symbol} Stock Price Trend ({data.index.min().date()} - {data.index.max().date()})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save chart to file instead of showing it
    chart_file = f"{symbol}_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(chart_file)
    print(f"Chart saved to: {chart_file}")

    # Save analysis results to CSV
    output_file = f"{symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    data.to_csv(output_file)
    print(f"Analysis saved to: {output_file}")

if __name__ == "__main__":
    # Use default symbol or override via command-line argument
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    analyze_stock(symbol)
