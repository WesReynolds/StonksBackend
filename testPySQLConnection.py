import mysql.connector

# Establish a connection
cnx = mysql.connector.connect(user='root', password='Valentino46', database='firstDB')

# Create a cursor
cur = cnx.cursor(buffered=True)

# Define queries
query = ("INSERT INTO firstTable VALUES (101, 102, 103)")
query2 = ("SELECT * FROM firstTable WHERE col2=102")

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
