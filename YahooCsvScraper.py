import os
import requests
import time
import pandas as pd


# Read the Ticker.csv file to get a list of stock symbols
def read_ticker_file(filename):
    tickers = []
    with open(filename, 'r') as file:
        for line in file:
            tickers.append(line.strip())
    return tickers


# Download .csv files from Yahoo Finance links, User-Agent added as Yahoo wasn't allowing me to scrape data otherwise
def download_csv(tickers):
    error_log = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    if not os.path.exists("historical_data"):
        os.makedirs("historical_data")

    for ticker in tickers:
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
        params = {
            "period1": 1460678400,  # Start date in UNIX timestamp (2016-04-15)
            "period2": 1655942400,  # End date in UNIX timestamp (2022-06-22)
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()


            filepath = os.path.join("historical_data", f"{ticker}.csv")
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {ticker}.csv")
        except Exception as e:
            error_log.append((ticker, str(e)))
            print(f"Error downloading {ticker}.csv: {str(e)}")

        # Add a delay to avoid rate limiting
        time.sleep(1)

    if error_log:
        print("\nErrors encountered for the following tickers:")
        for ticker, error_msg in error_log:
            print(f"{ticker}: {error_msg}")


# Combine .csv files into a single file with an added column for stock symbol
def combine_csv_files(tickers):
    combined_data = []

    for ticker in tickers:
        filepath = os.path.join("historical_data", f"{ticker}.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['StockSymbol'] = ticker
            combined_data.append(df)

    combined_df = pd.concat(combined_data, ignore_index=True)
    combined_df.to_csv("combined_data.csv", index=False)
    print("Combined data saved as 'combined_data.csv'")


if __name__ == "__main__":
    ticker_filename = "Ticker.csv"

    if os.path.exists(ticker_filename):
        tickers = read_ticker_file(ticker_filename)
        download_csv(tickers)
        combine_csv_files(tickers)
    else:
        print(f"Ticker file '{ticker_filename}' not found.")
