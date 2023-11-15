import mysql.connector

def connect():
    con = mysql.connector.connect(
        host='localhost',
        username='root',
        passwd='noobpes',
        database='e_commerce'
    )

    return con
