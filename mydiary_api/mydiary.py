"""
This module holds the app's datastructures and the different classes used
"""

# -*- coding: utf-8 -*-

"""importing packages"""
import datetime
from random import randrange
now = datetime.datetime.now()
from db_mydiary import db
from mydiary_api.app import app_db, my_diary_object
import jwt


""" the diary app is modelled as an object with it's own \
parameters and methods """
class MyDiary:
    def __init__(self):
        self.user_list = {}
        self.current_user = None    #current user's id
        self.user_entries = None
        self.user_index = 1

    def getUser(self, user_id)
        app_db.cursor.execute("SELECT * from entries WHERE user_id = %s;")
        row = app_db.cursor.fetchall()
        user = {
            user_id = row[0],
            name = row[1],
            email = row[2],
            password = row[3]
        }
        return user

    def addUser(self, user):
        user_id : user_index,
        user_name : user[name_data],
        user_email : user[email_data],
        user_password : user[password_data]

        app_db.cursor.execute("SELECT * from entries WHERE email = %s AND name = %s", (user_email, user_name))
        rows = app_db.cursor.fetchall()
        if rows[0] == []
            app_db.cursor.execute("INSERT INTO users (user_id, name, email, password) VALUES(%s,%s,%s,%s)", (user_id,user_name,user_email,user_password))
            message = "added successfully"
        else:
            message = "This user already exists!"
        return message
    

    def login(self, login_email, login_password):
        """ login method requires a username and password """
        app_db.cursor.execute("SELECT * from entries WHERE email = %s AND password = %s", (login_email, login_password))
        rows = app_db.cursor.fetchall()
        if rows == []:
            message = "Sorry, incorrect credentials"
        else:
            self.current_user == rows[0]
            message = "You've been logged in successfully"
        return message

    def logout(self):
        """ logout method clears the currentUser and userEntries \
        variables """
        if self.current_user != None:
            self.current_user = None
            self.user_entries = None
        else:
            print("Nobody logged in!")


class Users:
    """ All information about a user is stored in the User object """

    def __init__(self, name, email, password, my_diary_object):
        self.user_id = 
        self.current_user
        self.entries = Entries()
        self.user_index = 1
        my_diary_object.addUser(self)

    # def encode_auth_token(self, user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         payload = {
    #             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
    #             'iat': datetime.datetime.utcnow(),
    #             'sub': user_id
    #         }
    #         return jwt.encode(
    #             payload,
    #             app.config.get('SECRET_KEY'),
    #             algorithm='HS256'
    #         )
    #     except Exception as e:
    #         return e


    def __str__(self):
        user_details = [self.name, " ", self.email, " ", self.password]
        return "". join(user_details)

class Entries:
    """ Entry lists for each user are modelled as objects with \
    parameters and methods """

    def __init__(self):
        self.entry_index = 1
        self.entry_list = []
        self.all_entries = 0
        self.current_entries = 0
        self.deleted_entries = 0

        app_db.cursor.execute("SELECT * from entries;")
        rows = app_db.cursor.fetchall()
        self.current_entries = len(rows)
        self.all_entries = self.entry_index

    def addEntry(self, entry_id_data, user_id_data, title_data, entry_data, current_time):
        """ once a diary entry is created it sends itself to \
        Entries to be added to entrylist """
        entry_id = self.entry_index
        self.entry_index += 1
        user_id = user_id_data
        title = title_data
        data = entry_data
        date = current_time
        app_db.cursor.execute("INSERT INTO entries (entry_id, user_id, title, data, date) VALUES(%s,%s,%s,%s,%s)", (entry_id,user_id,title,data,date))
        

    def modifyEntry(self, title, data, date, user_id, entry_id):
        """ this method edits diary entries """
        app_db.cursor.execute("UPDATE entries SET title = %s, data = %s, date = %s) WHERE user_id = %s AND entry_id = %s;")

    def deleteEntry(self, user_id, entry_id):
        """ this method deletes diary entries """
        app_db.cursor.execute("DELETE from entries where user_id = %s AND entry_id = %s;")
        self.deleted_entries += 1

    def getOneEntry(self, user_id, entry_id):
        app_db.cursor.execute("SELECT * from entries WHERE user_id = %s AND entry_id = %s;")
        row = app_db.cursor.fetchone()
        entry = {
            'entry_id':row[0], 
            'user_id':row[1], 
            'title':row[2],
            'data':row[3],
            'date':row[4]
            }
        return entry

    def getAllEntries(self):
        app_db.cursor.execute("SELECT * from entries WHERE user_id = %s;")
        rows = app_db.cursor.fetchall()
        self.entry_list = []
        for row in rows:
            entry = {
            'entry_id':row[0], 
            'user_id':row[1], 
            'title':row[2],
            'data':row[3],
            'date':row[4]
            }
            self.entry_list.append(entry)
            return self.entry_list

    def __str__(self):
        """ this method displays a diary entry as a string """
        entry_string = ""
        for entry in self.entry_list:
            entry_string += entry.data +  " "  
        return entry_string

""" A DiaryEntry is stored as an object and it adds itself \
to the entry list """
class DiaryEntry:
    def __init__(self, entry_list, data, current_time=now):
        self.entry_id = entry_list.entry_index
        self.created = "".join(str(now.day)+"/"+str(now.month)\
                        +"/"+str(now.year))
        self.modified = "".join(str(now.day)+"/"+str(now.month)\
                        +"/"+str(now.year))
        self.entry_list = entry_list
        self.data = data
        self.entry_list.createEntry(self)

    def edit(self, entry_content, current_time=now):
        """ this method edits diary entry's data """
        self.data = entry_content
        self. modified = current_time
        self.entry_list.modifyEntry(self)
