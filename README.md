# Cramer-Backtesting

This project aimed to see whether or not Jim Cramer's calls, be it his calls verbatim or the opposite, would be able to outperform the market.

# Files
NOTE: Some files are too large to post in here (i.e. the historical data and other .csv files. They can be found in Google Drive here: https://drive.google.com/drive/folders/1i-hRHvTAsoIa59eUg8r9IjhrvTx7-i_h?usp=sharing

# Background

The rules for the project were the following:
1. The stocks had to still be on the market (not delisted) as of August 2023.
2. The data was grabbed off of the Mad Money Screener (https://madmoney.thestreet.com/screener/index.cfm?resetall=Y). This showed Cramer's calls on Mad Money between 4/18/2016 and 6/15/2022.
3. Returns were calculated off of adjusted close, not close, to account for dividends and splits, as many likely occurred between 2016-2022.
4. The calls were divided into 5 sections = All Calls, Small Cap Stocks Only, Mid Cap Stocks Only, Small and Mid Cap Stocks only, and Large Cap Stocks Only.
5. The data was then summarized into 3 separate sections:
  a. Market Cap (All Calls, Small Cap, Mid Cap, Small and Mid Cap, and Large Cap)
  b. Sector (Basic Materials, Communication Services, Consumer Cyclical, Consumer Defensive, Energy, Financial, Healthcare, Industrial, Real Estate, Tech, and Utilities)
  c. Region (LATAM, EU, China, Asia, US)
7. A trade would be entered the day Cramer announced it on Mad Money, and sold only when the opposite call was made, or on 6/15/2022, when data ends.

In order to grab the data, the following was done:
1. Data was scraped from the Mad Money Screener (Scraper.py)
2. Combine the .csv files from each day into 1 file (CSV_Combiner.py)
3. Then, clean the data by removing any delisted stocks (CSVCleaner.py)
4. Scrape data from Yahoo Finance for adjusted close data (HistoricalData.py)
5. Update the close price to adjusted close instead (this was done via SQL and Excel).

Once data was grabbed, the results were calculated in Excel (Inverse_Cramer_FINAL.xlsx).

# Results
The results surprised me personally, as none of them even came close to beating the market. In addition, all of the strategies produced single-digit percent returns over 6 years, which is incredibly low. 

![image](https://github.com/SBadovych/Cramer-Backtesting/assets/138629334/2cb0513c-a1a0-4630-9aa5-c83e871f7da7)

Some interesting insights could be found in the data as well:
1. In terms of Market Cap, Cramer seemed to succeed in Large Cap stocks primarily.
2. In terms of Sector, Tech and Financial were his best, while Real Estate and Energy were his worst.
3. In terms of Region, a couple of interesting insights pop up here. His returns in LATAM and Asia mimicked benchmark returns, with ILF and EZU being the benchmarks respectively. His worst regions are China and the US, being heavily behind benchmarks MCHI and SPY respectively.
4. His picks were primarily Large Cap stocks, making up over half of his picks. Filtering by sector shows a very diversified portfolio, with Tech and Consumer Cyclical stocks being the largest share. Filtering by region shows it being dominated by domestic stocks, making up nearly 94% of the picks.
5. Although he performed the best in Tech stocks, he still underperformed SPY by just under 70%.

I believe that the results could have been affected by a number of reasons, but here are some of the following:
1. Entry and exit prices could be delayed as Mad Money airs in the evening, meaning a trade would need to be executed the next morning, and that could lead to large changes in entry/exit prices.
2. The market was in a bull market for most of the time between 2016-2020, and the COVID recovery in 2020-2022 saw unprecedented returns.
3. Time is on Cramer's side here, as some trades were held for almost 6 years, in which a Buy call would be heavily slated to perform in his favor.


# Other Notes
It would be interesting to see how Cramer's strategy would play out in the following cases:
1. If a trade would be closed after 90/180/365 days instead of holding it until the opposite trade.
2. To see how Cramer's calls perform since 6/15/2022 until today, with the market having both a bull market and a bear market since that period. 
