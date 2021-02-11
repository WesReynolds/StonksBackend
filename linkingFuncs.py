import yfinance as yf
from flask import Flask
from flask_cors import CORS
from flask import jsonify
import mysql.connector
import datetime 

app = Flask(__name__)
CORS(app)

#gets next valid id  
def get_nxtId(cur):
    cur.execute("SELECT * FROM Users ORDER BY id DESC")
    return cur.fetchone()[0] + 1

def get_id(username, cur):
    cur.execute("SELECT * FROM Users WHERE username='%s'" % (username))
    fetch = cur.fetchone()
    if fetch == []:
        return None
    return fetch[0]
        
 
# Given customer information (first, last, username, password) 
# Will create a user in the user database and store information
@app.route("/c_acc/<first>/<last>/<username>/<password>", methods=['GET'])
def create_account(first, last, username, password):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # Look to see if username is already there 
    cur.execute("SELECT * FROM Users WHERE username='%s'" % (username))
    if (cur.fetchall() != []):
        return { 'Action': False }
    id = get_nxtId(cur)
    # Make change to database
    cur.execute("INSERT INTO Users Values ('%d', '%s', '%s', '%s', '%s')" % (id, username, password, first, last))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return { 'Action': True }

# Given customer information (username, password)
# Will return true if username and password work 
# Return false if not 
@app.route("/login/<username>/<password>", methods=['GET'])
def login(username, password):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # Look to see if username is already there 
    cur.execute("SELECT * FROM Users WHERE username='%s' AND password='%s'" % (username, password))
    if (cur.fetchall() == []):
        return { 'Action': False }
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return { 'Action': True }

#
# Assume Funds
# Action = BUY or SELL - all caps 
# Transactions  UserId, ticker, volume, action, price, time 
@app.route("/rec_t/<username>/<amount>/<tik>/<action>", methods=['GET'])
def record_transaction(username, amount, tik, action):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # get current price
    price =  search_tiker(tik).get('price')
    if(price == {}):
        return { 'Action': False}
    id = get_id(username, cur)
    if (id ==  None):
        return { 'Action': False}   
    time = datetime.datetime.now()
    
    cur.execute("INSERT INTO Transactions Values ('%d', '%s', '%d', '%s', '%f', '%s')" % (
        id, tik, amount, action, price, time))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return { 'Action': True}    

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
            return {}
            
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