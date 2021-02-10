import yfinance as yf
from flask import Flask
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)
# To Do:

# Given a Ticker symbol and Timestring, this function will
# return an Ordered Tuple of the form for the time frame:
# (currentPrice, lowPrice, highPrice)

@app.route("/tik/<tik>", methods=['GET'])
# search_tiker - send back tuple (boolean, current price(float))
def search_tiker(tik):
    try:
        stock = yf.Ticker(tik)
        return { 'price': stock.info.get("ask") }
    except:
        return {}

def get_interval(per):
    if(per == '1d'):
        return '60m'
    elif(per == '1mo'):
        return '1d'
    elif(per == '1y'):
        return '1wk'


# viewDetail_info -  
#   takes in: time period, tiker
#   return: current price, high and low of the period 

@app.route("/det/<per>/<tik>", methods=['GET'])
def viewDetail_info(per, tik):
        curr_price = search_tiker(tik)
        if curr_price == -1:
            return { }
            
        data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = tik,
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            period = per,
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            interval = get_interval(per),
            auto_adjust = True,
            prepost = True,
            threads = True,
            proxy = None
        )
        return { 'curr_price': curr_price, 'data_low': data['Low'][0], 'data_high': data['High'][-1] }

# graph_info 
#   takes in: time period, tiker, interval 
#   return: high and low in an array of ordered tuple 

@app.route("/graph/<per>/<tik>", methods=['GET'])
def graph_info(per, tik):
        curr_price = search_tiker(tik)
        if curr_price == -1:
            return { }
            
        data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = tik,
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            period = per,
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            interval = get_interval(per),
            auto_adjust = True,
            prepost = True,
            threads = True,
            proxy = None
        )
        result = []
        for entry in range(len(data['Low'])):
            result.append((data['Low'][entry], data['High'][entry]))
        return { 'days': result}

########################################################################################

def getDetailedStats(tckr, time):
    currentPrice = 0
    lowPrice = 0
    highPrice = 0
    return (currentPrice, lowPrice, highPrice)


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