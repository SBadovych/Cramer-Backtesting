import pandas as pd
import csv
import datetime

input_xlsx_file = "Inverse_Cramer_FINAL.xlsx"
sheet_name = "Calls"
df_entries = pd.read_excel(input_xlsx_file, sheet_name=sheet_name)

adj_close_csv_file = "combined_data.csv"
adj_close_data = {}
with open(adj_close_csv_file, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ticker = row["StockSymbol"]
        date = row["Date"]
        adj_close_str = row["Adj Close"]
        if adj_close_str:  # Check if the value is not empty
            adj_close = float(adj_close_str)
            if ticker not in adj_close_data:
                adj_close_data[ticker] = {}
            adj_close_data[ticker][date] = adj_close

output_data_sheet1 = []
output_data_sheet2 = []
for idx, entry in df_entries.iterrows():
    entry_date = entry["Entry Date"]
    exit_date = entry["Exit Date"]
    ticker = entry["Ticker"]

    print(f"Processing entry {idx + 1}: Ticker = {ticker}, Entry Date = {entry_date}, Exit Date = {exit_date}")

    current_date = entry_date
    while current_date <= exit_date:
        # Exclude weekends (Saturday and Sunday)
        if current_date.weekday() < 5:  # Monday to Friday
            formatted_date = current_date.strftime("%Y-%m-%d")
            if ticker in adj_close_data and formatted_date in adj_close_data[ticker]:
                adj_close = adj_close_data[ticker][formatted_date]
                output_row = {
                    "Entry Date": entry_date,
                    "Exit Date": exit_date,
                    "Ticker": ticker,
                    "Date": formatted_date,
                    "Adj Close": adj_close
                }
                if idx % 2 == 0:
                    output_data_sheet1.append(output_row)
                else:
                    output_data_sheet2.append(output_row)
                print(f"  Date: {formatted_date}, Adj Close: {adj_close}")
        current_date += datetime.timedelta(days=1)

df_output_sheet1 = pd.DataFrame(output_data_sheet1)
df_output_sheet2 = pd.DataFrame(output_data_sheet2)

output_xlsx_file = "HistoricalData.xlsx"
with pd.ExcelWriter(output_xlsx_file) as writer:
    df_output_sheet1.to_excel(writer, sheet_name="Sheet1", index=False)
    df_output_sheet2.to_excel(writer, sheet_name="Sheet2", index=False)
print("Output saved to", output_xlsx_file)
