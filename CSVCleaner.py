import pandas as pd
import yfinance as yf
from requests.exceptions import HTTPError

def clean_csv(input_file, output_file):
    print("Reading the input CSV file...")
    try:
        # Step 1: Read the CSV file and remove the "Portfolio" and "Segment" columns
        df = pd.read_csv(input_file)
        df.drop(columns=["Portfolio", "Segment"], inplace=True)
        print("Successfully removed 'Portfolio' and 'Segment' columns.")
    except Exception as e:
        print(f"Error occurred while reading and removing columns: {str(e)}")
        return

    # Step 2: Rename "FB" cells to "META"
    print("Renaming 'FB' cells to 'META'...")
    df.replace("FB", "META", inplace=True)
    print("Successfully renamed 'FB' cells to 'META'.")

    # Step 3: Check if the stock is accessible via Yahoo Finance and remove the rows with 404 errors
    print("Checking stock accessibility...")
    tickers = df["Ticker"].tolist()
    valid_tickers = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            # Accessing any attribute to check if the stock is accessible
            stock.info
            valid_tickers.append(ticker)
        except HTTPError as e:
            if e.response.status_code == 404:
                print(f"Stock '{ticker}' not found. Removing from the dataset.")
            else:
                print(f"Error occurred while checking stock '{ticker}': {str(e)}")
        except Exception as e:
            print(f"Error occurred while checking stock '{ticker}': {str(e)}")
            continue

    df = df[df["Ticker"].isin(valid_tickers)]
    print("Stock accessibility checked and invalid stocks removed successfully.")

    # Step 4: Export cleaned data to a new CSV file
    print("Exporting cleaned data to a new CSV file...")
    try:
        df.to_csv(output_file, index=False)
        print("Data exported to the new CSV file successfully.")
    except Exception as e:
        print(f"Error occurred while exporting the data: {str(e)}")

if __name__ == "__main__":
    input_file = "CramerCalls.csv"
    output_file = "cleaned_output.csv"
    clean_csv(input_file, output_file)
