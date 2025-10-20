import mysql.connector
import os

db_config = {
    "user": "root",            # please remember to change this to your MySQL username
    "password": "mypassword",  # please remember to change this to your MySQL password
    "host": "127.0.0.1",       # use localhost since MySQL is local
    "database": "nyc_taxi_db"
}



def fetchall(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
