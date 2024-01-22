import mysql.connector

def db_connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ppcreveal_niche_detector"
    )
    return mydb
    