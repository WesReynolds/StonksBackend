import yfinance as yf
from flask import Flask
from flask_cors import CORS
from flask import jsonify
import mysql.connector
import datetime 
import requests
import ssl

app = Flask(__name__)
CORS(app)
ssl._create_default_https_context = ssl._create_unverified_context

#gets next valid id
def get_nxtId(cur):
    cur.execute("SELECT * FROM Users ORDER BY id DESC")
    nxtID = cur.fetchone()
    # makes sure there is something in database
    if nxtID is None:
        return 1
    else:
        return nxtID[0] + 1

def get_id(username, cur):
    cur.execute("SELECT * FROM Users WHERE username='%s'" % (username))
    fetch = cur.fetchone()
    if fetch == None:
        return None
    return fetch[0]

def add_to_cache(tik):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)

    cur.execute("SELECT * FROM Cache WHERE Ticker='%s'" % (tik))
    if cur.fetchall() == []:
        stock = search_tiker(tik)
        price = stock.get("Price")
        dayHigh = stock.get("DayHigh")
        dayLow = stock.get("DayLow")
        percChange = stock.get("PercentChange")
        volume = stock.get("Volume")
        shortName = stock.get("shortName")
        if price is not None and dayHigh is not None and dayLow is not None and percChange is not None and \
                volume is not None:
            cur.execute("INSERT INTO Cache Values ('%s', '%f', '%s', '%f', '%f', '%f', '%d', '%s')" %
                    (stock.get("Ticker"), price, stock.get("Sector"), dayHigh,
                    dayLow, percChange, volume, shortName))
    cnx.commit()
    # Close connections 
    cnx.close()
    return { 'Action': True }

@app.route("/buy/<username>/<tik>/<volume>")
def buy(username, tik, volume):
    volume = int(volume)
    if (volume <= 0):
        return {'success' : False, 'error' : 99}
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # get current price
    price =  search_tiker(tik).get('Price')
    if(price == None or price == 0):
        return {'success' : False, 'error' : 98}
    id = get_id(username, cur)
    if (id ==  None):
        return {'success' : False, 'error' : 97}
    time = datetime.datetime.now()
    cur.execute("INSERT INTO Transactions Values ('%d', '%s', '%d', 'BUY', '%f', '%s', 0)" % (
        id, tik, volume, price, time))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    add_to_cache(tik)
    return {'success' : True}

@app.route("/sell/<username>/<tik>/<volume>")
def sell(username, tik, volume):
    volume = int(volume)
    if (volume <= 0):
        return {'success' : False, 'error' : 99}
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # get current price
    price =  search_tiker(tik).get('Price')
    if(price == {}):
        return {'success' : False, 'error' : 98}
    id = get_id(username, cur)
    if (id ==  None):
        return {'success' : False, 'error' : 97}
    time = datetime.datetime.now()
    cur.execute("SELECT * FROM Transactions WHERE ticker='%s' AND UserId='%d'" % (tik, id))
    curVolume = 0
    fetch = cur.fetchall()
    if fetch == []:
        return {'success': False, 'error': 96}
    for item in fetch:
        if item[3] == "BUY":
            curVolume += item[2]
        else:
            curVolume -= item[2]
    if volume > curVolume:
        return {'success' : False, 'error' : 95}
    
    cur.execute("INSERT INTO Transactions Values ('%d', '%s', '%d', 'SELL', '%f', '%s', 0)" % (id, tik, volume, price, time))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return {'success' : True}


@app.route("/g_prof/<username>", methods=['GET'])
def get_profile(username):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    id = get_id(username, cur)
    #get transactions
    cur.execute("SELECT * FROM Transactions WHERE UserId='%d' ORDER BY ticker" % (id))
    fetch = cur.fetchall()
    if (fetch == []):
        return { 'Action': False }
    ret = {}
    oldTik = ""
    volume = 0
    totalSpent = 0
    key = 0
    p_value = 0
    p_change = 0
    p_spent = 0
    for result in fetch:
        if result[1] != oldTik:
            if totalSpent != 0:
                curPrice =  search_tiker(oldTik).get('Price')
                posValue = round((volume * curPrice), 2)
                percentChange = round(((posValue - totalSpent) / totalSpent) * 100, 2)
                ret[key] = {"ticker": oldTik, "price" : curPrice, "volume": volume, "percentage": percentChange,
                            "posValue" : posValue}
                p_value = p_value + posValue
                p_spent = p_spent + totalSpent
                key = key + 1
                volume = totalSpent = 0
        if result[3] == "SELL":
            volume -= result[2]
            totalSpent -= (result[4] * result[2])
        else:
            volume += result[2]
            totalSpent += (result[4] * result[2])
        oldTik = result[1]

    curPrice = search_tiker(oldTik).get('Price')
    if totalSpent != 0:
        posValue = round((volume * curPrice), 2)
        percentChange = round(((posValue - totalSpent) / totalSpent) * 100, 2)
        p_value = round((p_value + posValue), 2)
        p_spent = p_spent + totalSpent
        p_change = round(((p_value - p_spent) / p_spent) * 100, 2)
        ret[key] = {"ticker": oldTik, "price" : curPrice, "volume": volume, "percentage": percentChange,
                    "posValue" : posValue, "total" : p_value, "totalChange" : p_change}
    # Commit change
    cnx.commit()
    # Close connections
    cnx.close()
    return ret

@app.route("/g_watch/<username>", methods=['GET'])
def get_watchlist(username):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    id = get_id(username, cur)
    #get transactions
    cur.execute("SELECT * FROM Transactions WHERE UserId='%d' AND volume=0 AND display=1 ORDER BY ticker" % (id))
    ret = {}
    key = 0
    for stock in cur.fetchall():
        price = search_tiker(stock[1]).get('Price')
        ret[key] = {"ticker": stock[1], "price": price}
        key = key + 1
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return ret

# Takes in string of trending stock information 
# Returns: dictionary information of stocks
def get_trending_dict(string):
    retDict = {}
    index = string.find("symbol")
    index += 9
    ticker = ""
    i = 0
    while i < 5:
        while string[index] != '"':
            ticker += string[index]
            index += 1
        retDict[i] = {"ticker" : ticker, "price" : search_tiker(ticker).get("Price")}
        index = string.find("symbol", index)
        index += 9
        ticker = ""
        i+=1
    return retDict

# returns a dictionary of the trending data
@app.route("/g_trend", methods=['GET'])
def get_trending():
    # Request the new api 
    # Returns string of trending stock info
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"
    querystring = {"region":"US"}
    headers = {
        'x-rapidapi-key': "9a2781c23bmsh7f295aceb2c0a9ap18232ejsnbaec90b0a568",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    # Returns dictionary of trending stocks  
    overall = get_trending_dict(response.text)
    return overall

# Takes in string of trending stock information 
# Returns: dictionary information of stocks
def get_movers_dict(string, amount):
    retDict = {}
    index = string.find("symbol")
    index += 9
    ticker = ""
    i = 0
    while i < amount:
        while string[index] != '"':
            ticker += string[index]
            index += 1
        retDict[i] = {"ticker" : ticker, "price" : search_tiker(ticker).get("Price")}
        index = string.find("symbol", index)
        index += 9
        ticker = ""
        i += 1
    return retDict

# returns a dictionary of the biggest moving data
@app.route("/g_move", methods=['GET'])
def get_movers():
    # Request the new api 
    # Returns string of trending stock info
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"
    querystring = {"region":"US","lang":"en-US","start":"0","count":"6"}

    headers = {
        'x-rapidapi-key': "9a2781c23bmsh7f295aceb2c0a9ap18232ejsnbaec90b0a568",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # Returns dictionary of trending stocks  
    overall = get_movers_dict(response.text, 5)
    return overall


# Given customer information (first, last, username, password) 
# Will create a user in the user database and store information
@app.route("/c_acc/<first>/<last>/<username>/<password>", methods=['GET'])
def create_account(first, last, username, password):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
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
    resp = jsonify(success=True, username=username, firstname=first, lastname=last,
                   password=password)
    resp.status_code = 201
    return resp

# Given customer information (username, password)
# Will return true if username and password work 
# Return false if not 
@app.route("/login/<username>/<password>", methods=['GET'])
def login(username, password):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # Look to see if username is already there 
    cur.execute("SELECT * FROM Users WHERE username='%s' AND password='%s'" % (username, password))
    userSQL = cur.fetchall()
    if (userSQL == []):
        return { 'Action': False }
    # json user profile
    resp = jsonify(success=True, username=userSQL[0][1], firstname=userSQL[0][3],
                  lastname=userSQL[0][4], password=userSQL[0][2])
    resp.status_code = 201
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return resp

# returns json form of all users in mySQL DB
# FOR DEV PURPOSES - MAY NOT BE USED IN FINAL SHIP
@app.route("/users", methods=['GET'])
def get_users():
    users = {
        'users_list' :
            [

            ]
    }
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor
    cur = cnx.cursor(buffered=True)
    # fetch all users in DB
    cur.execute("SELECT * FROM Users")
    userSQL = cur.fetchall()
    for user in userSQL:
        userJson = {"username" : user[1],
                    "firstname" : user[3],
                    "lastname" : user[4],
                    "password" : user[2]}
        users['users_list'].append(userJson)
    # Commit change
    cnx.commit()
    # Close connections
    cnx.close()
    return users

@app.route("/rem_w/<username>/<tik>", methods=['GET'])
def remove_watchlist(username, tik):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # get current price
    price =  search_tiker(tik).get('Price')
    if(price == {}):
        return { 'Action': False }
    id = get_id(username, cur)
    if (id ==  None):
        return { 'Action': False }   
    time = datetime.datetime.now()
    cur.execute("INSERT INTO Transactions Values ('%d', '%s', 0, 'SELL', '%f', '%s', 0)" % (id, tik, price, time))
    cur.execute("UPDATE Transactions SET display=0 WHERE ticker='%s' AND volume=0 AND display=1" % (tik))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return { 'Action': True}
 
# Assume Funds
# Action = BUY or SELL - all caps 
# Transactions  UserId, ticker, volume, action, price, time 
@app.route("/add_w/<username>/<tik>", methods=['GET'])
def add_watchlist(username, tik):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # get current price
    price =  search_tiker(tik).get('Price')
    if(price == 0):
        return { 'Action': False}
    id = get_id(username, cur)
    if (id ==  None):
        return { 'Action': False}
    cur.execute("SELECT * FROM Transactions WHERE UserId='%d' AND volume=0 AND display=1 AND ticker='%s'" % (id, tik))  
    if cur.fetchone() != None:
        return { 'Action': False}
    time = datetime.datetime.now()
    if price == None:
        price = 0
    cur.execute("INSERT INTO Transactions Values ('%d', '%s', 0, 'BUY', '%f', '%s', 1)" % (
        id, tik, price, time))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    add_to_cache(tik)
    return { 'Action': True}

@app.route("/update_cache/", methods=['GET'])
def update_cache():
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    cur2 = cnx.cursor(buffered=True)
    cur.execute("SELECT DISTINCT * FROM Transactions ORDER BY ticker")
    tickerList = []
    for ticker in cur.fetchall():
        if not ticker[1] in tickerList:
            tickerList.append(ticker[1])
            stock = yf.Ticker(ticker[1])
            sector = stock.info.get("sector")
            dayHigh = stock.info.get("dayHigh")
            dayLow = stock.info.get("dayLow")
            wkChange = stock.info.get("52WeekChange")
            volume = stock.info.get("volume")
            price = stock.info.get("ask")
            shortName = stock.info.get("shortName")
            if (price == 0 or price == None):
                price = stock.info.get("dayClose")
            if price == None:
                price = 0
            if dayHigh == None:
                dayHigh = 0
            if dayLow == None:
                dayLow = 0
            if volume == None:
                volume = 0
            if wkChange == None:
                wkChange = 0
            cur2.execute("SELECT DISTINCT * FROM Cache WHERE ticker='%s'" % (ticker[1]))
            if cur2.fetchone() == None:
                cur.execute("INSERT INTO Cache Values ('%s', '%f', '%s', '%f', '%f', '%f', '%d', '%s')" %
                            (ticker[1], price, sector, dayHigh,
                            dayLow, wkChange, volume, shortName))
            else:
                cur.execute("UPDATE Cache SET Ticker='%s', Price='%f', Sector='%s', DayHigh='%f', DayLow='%f', "
                            "PercentChange='%f', Volume='%d', shortName='%s' WHERE Ticker='%s'" %
                            (ticker[1], price, sector, dayHigh,
                            dayLow, wkChange, volume, shortName, ticker[1]))
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return { 'Action': True}

@app.route("/tik/<tik>", methods=['GET'])
# search_tiker - send back dictionary 
def search_tiker(tik):
    # establish connection
    cnx = mysql.connector.connect(user='root', password='*password*', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)

    cur.execute("SELECT * FROM Cache WHERE Ticker='%s'" % (tik))
    
    fetch = cur.fetchone()
    if fetch == None:
        try:
            stock = yf.Ticker(tik)
            v = stock.info
        except:
            return { "Action": False }

        price = v.get("ask")
        if price == None or price == 0:
            price = stock.info.get("previousClose")
        sector = v.get("sector")
        dayHigh = v.get("dayHigh")
        if dayHigh == None:
            dayHigh = 0
        dayLow = v.get("dayLow")
        if dayLow == None:
            dayLow = 0
        change = v.get("52WeekChange")
        if change == None:
            change = 0
        volume = v.get("volume")
        if volume == None:
            volume = 0

        retDict = {"Name": stock.info.get("shortName"), "Ticker": tik , "Price": price, "Sector": sector,
                    "DayHigh": dayHigh, "DayLow": dayLow, "PercentChange": change, "Volume": volume}
    else:
        retDict = { "Name" : fetch[7], "Ticker": fetch[0], "Price": fetch[1], "Sector": fetch[2], "DayHigh": fetch[3], "DayLow": fetch[4],
                "PercentChange": fetch[5], "Volume": fetch[6]}
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return retDict

def get_interval(per):
    if(per == '1d'):
        return '60m'
    elif(per == '1mo'):
        return '1d'
    elif(per == '1y'):
        return '1wk'

