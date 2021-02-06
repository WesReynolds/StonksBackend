from yahoofinance import HistoricalPrices
import yfinance as yf
from yahoo_finance import Share

# print(HistoricalPrices("MSFT", "2021-02-02", "2021-02-04").to_dfs())

# print(msft.info.get("ask"))



def ticker_push(tik):
    msft = yf.Ticker(tik)

#tik = string 
def data_stream(tik, interval):
    data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = tik,
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            period = "3mo",
            
            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = "1d",

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy = None
        )

# print(data['High'][0]) # Prints the High value of the term specified
# print(data['High'][1]) 

for day in data['High']:
    print(day)

# print(data['Low'][0])  # Prints the Low value of the term specified



#print(msft.info)
#print(msft.info.get("regularMarketPrice"))

# Dictionary 
# dayHigh - day high 
# dayLow -  day low 
# regularMarketPrice - avg market price 
# bid - what they want to buy for 
# *ask - what they want to sell for 