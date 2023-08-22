import requests
from bs4 import BeautifulSoup
import csv
import os
import re

# Define the starting and ending values for the airdate value
start_value = 42478
end_value = 44727

# Create the folder for storing CSV files
folder_name = "CSV Files"
os.makedirs(folder_name, exist_ok=True)

# Loop through the URLs for the range above
for value in range(start_value, end_value + 1):
    # Specify the URL with the updated airdate value
    url = f'https://madmoney.thestreet.com/screener/index.cfm?showview=stocks&showrows=500&airdate={value}'

    # Make a GET request to fetch the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table element with the id "stockTable" to scrape
    table = soup.find('table', {'id': 'stockTable'})

    # Check if the table contains the "Sorry, no stocks were found" message, meaning no show aired that day
    if table and "Sorry, no stocks were found that match your criteria." in table.text:
        print(f"No stocks found for {url}. Skipping to the next iteration.")
        continue

    # Initialize lists to store the table data
    data = []
    header = ["Company", "Ticker", "Date", "Segment", "Call", "Price", "Portfolio"]

    # Extract the table rows
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        row_data = []
        cells = row.find_all('td')

        # Extract table header if it's the first row
        if i == 0:
            continue  # Skip the first row (header row)
        else:
            for j, cell in enumerate(cells):
                if j == 0:  # Company Column
                    company_name = cell.text.strip()
                    ticker = re.search(r'\((.*?)\)', company_name).group(1)
                    company_name = re.sub(r'\s*\([^()]*\)', '', company_name)
                    row_data.append(company_name)
                    row_data.append(ticker)
                elif j == 2 or j == 3:  # Segment and Call Columns, the Alt value makes it readable, as the values are images
                    row_data.append(cell.find('img')['alt'].strip())
                else:
                    row_data.append(cell.text.strip())

            # Add to the "Date" column based on the airdate value
            year = None

            if 42478 <= value <= 42735:
                year = '/16'
            elif 42736 <= value <= 43100:
                year = '/17'
            elif 43101 <= value <= 43465:
                year = '/18'
            elif 43466 <= value <= 43830:
                year = '/19'
            elif 43831 <= value <= 44196:
                year = '/20'
            elif 44197 <= value <= 44561:
                year = '/21'
            else:
                year = '/22'

            row_data[2] += year  # Date Column + Year

            # Label the "Call" column values as "SELL", "NEUTRAL", or "BUY"
            call_value = int(row_data[4])  # Call Column
            if call_value == 1 or call_value == 2:
                row_data[4] = "SELL"
            elif call_value == 3:
                row_data[4] = "NEUTRAL"
            elif call_value == 4 or call_value == 5:
                row_data[4] = "BUY"

            data.append(row_data)

    # Export the data into a CSV file
    if data:
        csv_file = os.path.join(folder_name, f'Cramer_Calls_{value}.csv')
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)

        print(f"Data has been saved to {csv_file}.")
    else:
        print(f"No data found for {url}. Skipping....")
