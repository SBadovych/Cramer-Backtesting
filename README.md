# Cramer-Backtesting

This project aimed to see whether or not Jim Cramer's calls, be it his calls verbatim or the opposite, would be able to outperform the market.

# Background

The rules for the project were the following:
1. The stocks had to still be on the market (not delisted) as of August 2023.
2. The data was grabbed off of the Mad Money Screener (https://madmoney.thestreet.com/screener/index.cfm?resetall=Y). This showed Cramer's calls on Mad Money between 4/18/2016 and 6/15/2022.
3. Returns were calculated off of adjusted close, not close, to account for dividends and splits, as many likely occurred between 2016-2022.
4. The calls were divided into 5 sections = All Calls, Small Cap Stocks Only, Mid Cap Stocks Only, Small and Mid Cap Stocks only, and Large Cap Stocks Only.
5. A trade would be entered the day Cramer announced it on Mad Money, and sold only when the opposite call was made, or on 6/15/2022, when data ends.

In order to grab the data, the following was done:
1. Data was scraped from the Mad Money Screener (Scraper.py)
2. Combine the .csv files from each day into 1 file (CSV_Combiner.py)
3. Then, clean the data by removing any delisted stocks (CSVCleaner.py)
4. Scrape data from Yahoo Finance for adjusted close data (HistoricalData.py)
5. Update the close price to adjusted close instead (this was done via SQL and Excel).

Once data was grabbed, the results were calculated in Excel (Inverse_Cramer_FINAL.xlsx).

# Results
The results surprised me personally, as none of them even came close to beating the market. In addition, all of the strategies produced single-digit percent returns over 6 years, which is incredibly low. 

I believe that the results could have been affected by a number of reasons, but here are some of the following:
1. Entry and exit prices could be delayed as Mad Money airs in the evening, meaning a trade would need to be executed the next morning, and that could lead to large changes in entry/exit prices.
2. The market was in a bull market for most of the time between 2016-2020, and the COVID recovery in 2020-2022 saw unprecedented returns.
3. Time is on Cramer's side here, as some trades were held for almost 6 years, in which a Buy call would be heavily slated to perform in his favor.


# Other Notes
It would be interesting to see how Cramer's strategy would play out in the following cases:
1. If a trade would be closed after 90/180/365 days instead of holding it until the opposite trade.
2. To see how Cramer's calls perform since 6/15/2022 until today, with the market having both a bull market and a bear market since that period. 
