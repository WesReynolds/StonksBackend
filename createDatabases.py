
# Go to: 
# https://dev.mysql.com/downloads/mysql/
# follow download process for your machine
# set password to *password*

#How to run 
# 1). mysql -u root -p 
# 2). *password*
# 3). CREATE DATABASE StonkLabs
# 4). run script 
# 5). Enjoy! :)

import datetime 
import mysql.connector


# Does not reutrn anything.
# This method will create a "Users" Table for your
# current database, assuming the user is "root"
def create_users():
    # establish connection
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # Create the Users Table
    cur.execute("CREATE TABLE Users (id int, username varchar(255), password varchar(255), firstName varchar(255), lastName varchar(255))")    
    cur.execute("INSERT INTO Users Values (1, 'Wazza', 'myPassword', 'Wesley', 'Reynolds')")
    cur.execute("INSERT INTO Users Values (2, 'Joshi', 'lolz', 'Joshua', 'Ravioli')")
    cur.execute("INSERT INTO Users Values (3, 'Neeko', 'ripsSourins', 'Nicholas', 'Hansen')")
    cur.execute("INSERT INTO Users Values (4, 'Bonzo', 'cleanFade', 'Jon', 'Wallach')")
    cur.execute("INSERT INTO Users Values (5, 'Apples', 'loveme', 'Caroline', 'Reaper')")
    cur.execute("INSERT INTO Users Values (6, 'user345', 'terrible_pass', 'David', 'Vahnderhaar')")
    cur.execute("INSERT INTO Users Values (7, 'Godwin', 'purplewrap', 'Kelsi', 'Monroe')")
    cur.execute("INSERT INTO Users Values (8, 'WRLD999', 'juicey', 'Jarad', 'Gonzales')")
    cur.execute("INSERT INTO Users Values (9, 'Redd', 'trippie', 'James', 'Charles')")
    cur.execute("INSERT INTO Users Values(10, 'activist', 'uphere', 'Daquan', 'Rashad')")
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return
    
def create_transactions():
    # establish connection
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # Create the Transactions Table 
    cur.execute("CREATE TABLE Transactions(UserId int REFERENCES Users (id), ticker varchar(10), volume float(0), action varchar(5), price float(0), time DATETIME(0), display int)")
    time = datetime.datetime.now()
    cur.execute("INSERT INTO Transactions Values (1, 'AAPL', 10, 'BUY', 134.85, '%s', 1)" % time)
    cur.execute("INSERT INTO Transactions Values (1, 'AAPL', 2, 'SELL', 134.85, '%s', 0)" % time)
    cur.execute("INSERT INTO Transactions Values (3, 'AAPL', 10, 'BUY', 134.85, '%s', 1)" % time)
    cur.execute("INSERT INTO Transactions Values (7, 'AAPL', 7, 'SELL', 134.85, '%s', 0)" % time)
    cur.execute("INSERT INTO Transactions Values (7, 'GME', 12, 'BUY', 52.40, '%s', 1)" % time)
    cur.execute("INSERT INTO Transactions Values (7, 'GME', 12, 'SELL', 4.25, '%s', 0)" % time)
    cur.execute("INSERT INTO Transactions Values (2, 'AAPL', 10, 'BUY', 134.85, '%s', 1)" % time)
    cur.execute("INSERT INTO Transactions Values (2, 'AAPL', 10, 'BUY', 134.85, '%s', 1)" % time)
    cur.execute("INSERT INTO Transactions Values (10, 'AAPL', 10, 'BUY', 134.85, '%s', 1)" % time)
    cur.execute("INSERT INTO Transactions Values (10, 'AAPL', 10, 'BUY', 134.85, '%s', 1)" % time)
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return

def create_cache():
    # establish connection
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')
    # create a cursor 
    cur = cnx.cursor(buffered=True)
    # Create the Cache 
    cur.execute("CREATE TABLE Cache (Ticker varchar(10), Price float(0), Sector varchar(100), DayHigh float(0), DayLow float(0), PercentChange float(0), Volume int)")
    # Commit change 
    cnx.commit()
    # Close connections 
    cnx.close()
    return
    
def main():
    create_users()
    create_transactions()
    create_cache()
    return 0

main()




