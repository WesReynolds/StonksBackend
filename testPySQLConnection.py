import mysql.connector

# Establish a connection
cnx = mysql.connector.connect(user='root', password='Valentino46', database='StonkLabs')

# Create a cursor
cur = cnx.cursor(buffered=True)

# Define queries
query = ("INSERT INTO Users VALUES (3, 'Mike', 'RobbyLuv')")
query2 = ("SELECT * FROM Users WHERE id=3")

# Execute queries
#cur.execute(query)
cur.execute(query2)

# Fetch results of queries
#print(cur.fetchone()[1])
print(cur.fetchall())

# Commit changes
cnx.commit()

# Close connection
cnx.close()
