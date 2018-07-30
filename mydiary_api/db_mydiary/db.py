#!/usr/bin/python

from configparser import ConfigParser
import psycopg2


class MyDiary_Database:
    def __init__(self):
        try:
            self.connect_str = "dbname='mydiary_db' user='mydiary_user' " + \
                        "host='localhost' password='password' port='5432'"
            self.conn = psycopg2.connect(self.connect_str)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Unable to connect. Check dbname, user or password inputs.")
            print(e)

    def new_users_table(self):
        self.cursor.execute("""CREATE TABLE users 
                    (user_id INTEGER PRIMARY KEY, 
                    name VARCHAR(40) NOT NULL, 
                    email VARCHAR(60) NOT NULL, 
                    password VARCHAR(40) NOT NULL);""")
        self.conn.commit()
        #cursor.execute("""SELECT * from users""")
        #rows = cursor.fetchall()
        #print(rows)

    def new_entries_table(self):
        self.cursor.execute("""CREATE TABLE entries 
                    (entry_id INTEGER PRIMARY KEY, 
                    user_id INTEGER NOT NULL, 
                    title VARCHAR(20) NOT NULL, 
                    data VARCHAR(500) NOT NULL, 
                    date VARCHAR(10) NOT NULL);""")
        self.conn.commit()
