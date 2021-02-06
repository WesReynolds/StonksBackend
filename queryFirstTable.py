import sys
import mysql.connector

def main(argv):
    cnx = mysql.connector.connect(user='root', password='Valentino46', database='firstDB')

    cur = cnx.cursor(buffered=True)
    
    query = ("SELECT * FROM firstTable WHERE col1=%s or col2=%s or col3=%s" 
            % (argv[1], argv[1], argv[1]))

    cur.execute(query)

    for result in cur.fetchall():
        print(result)

    cnx.commit()

    cnx.close()

main(sys.argv)
