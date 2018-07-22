"""
This module holds the app's datastructures and the different classes used
"""

# -*- coding: utf-8 -*-

"""importing packages"""
import datetime
from random import randrange
now = datetime.datetime.now()

""" the diary app is modelled as an object with it's own \
parameters and methods """
class MyDiary:
    def __init__(self):
        self.user_list = {}
        self.current_user = None
        self.user_entries = None
    
    def addUser(self, user):
        """ User must be able to register """

        if user in list(self.user_list.values()): 
            return "User already exists"
        else:
            self.user_list[user.email] = user
        
    def login(self, login_email, login_password):
        """ login method requires a username and password """

        if self.user_list[login_email].password == login_password:
            self.current_user = self.user_list.get(login_email)
            self.user_entries = self.current_user.entries
        else:
            print("incorrect login credentials")
    
    def logout(self):
        """ logout method clears the currentUser and userEntries \
        variables """

        if self.current_user != None:
            self.current_user = None
            self.user_entries = None
        else:
            print("Nobody logged in!")


class User:
    """ All information about a user is stored in the User object """

    def __init__(self, name, email, password, my_diary_object):
        #self.userId = rand()
        self.name = name
        self.email = email
        self.password = password
        self.entries = Entries()
        my_diary_object.addUser(self)
        
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
        self.current_entries = len(self.entry_list)        
        self.deleted_entries = 0
        self.all_entries = self.entry_index
        
    def createEntry(self, DiaryEntry):
        """ once a diary entry is created it sends itself to \
        Entries to be added to entrylist """
        self.entry_list.append(DiaryEntry)
        self.entry_index += 1
        
    def modifyEntry(self, DiaryEntry):
        """ this method edits diary entries """
        for i in range(len(self.entry_list)-1):
            if self.entry_list[i].entry_id == DiaryEntry.entry_id:
                self.entry_list[i]=DiaryEntry 
    
    def deleteEntry(self, DiaryEntry):
        """ this method deletes diary entries """
        if DiaryEntry in list(self.entry_list):
            self.entry_list.pop(DiaryEntry.entry_id)
            self.deleted_entries += 1
    
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


def main():
    pass
    

if __name__ == '__main__':
    main()