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
        self.userlist = {}
        self.currentUser = None
        self.userEntries = None
    
    def addUser(self, user):
        """ User must be able to register """

        if user in list(self.userlist.values()): 
            return "User already exists"
        else:
            self.userlist[user.email] = user
        
    def login(self, loginEmail, loginPassword):
        """ login method requires a username and password """

        if self.userlist[loginEmail].password == loginPassword:
            self.currentUser = self.userlist.get(loginEmail)
            self.userEntries = self.currentUser.entries
        else:
            print("incorrect login credentials")
    
    def logout(self):
        """ logout method clears the currentUser and userEntries \
        variables """

        if self.currentUser != None:
            self.currentUser = None
            self.userEntries = None
        else:
            print("Nobody logged in!")


class User:
    """ All information about a user is stored in the User object """

    def __init__(self, name, email, password, mydiaryobject):
        #self.userId = rand()
        self.name = name
        self.email = email
        self.password = password
        self.entries = Entries()
        mydiaryobject.addUser(self)
        
    def __str__(self):
        user_details = [self.name, " ", self.email, " ", self.password]
        return "". join(user_details)
        
class Entries:
    """ Entry lists for each user are modelled as objects with \
    parameters and methods """

    def __init__(self):
        self.entryIndex = 1
        self.entrylist = []
        self.allEntries = None
        self.deletedEntries = None
        self.currentEntries = None
        
    def createEntry(self, DiaryEntry):
        """ once a diary entry is created it sends itself to \
        Entries to be added to entrylist """

        self.entrylist.append(DiaryEntry)
        self.entryIndex += 1
        
    def modifyEntry(self, DiaryEntry):
        """ this method edits diary entries """

        for i in range(len(self.entrylist)-1):
            if self.entrylist[i].entryId == DiaryEntry.entryId:
                self.entrylist[i]=DiaryEntry 
    
    def deleteEntry(self, DiaryEntry):
        """ this method deletes diary entries """

        if DiaryEntry in list(self.entrylist):
            self.entrylist.pop(DiaryEntry.entryId)
    
    def __str__(self):
        """ this method displays a diary entry as a string """
        entrystring = ""
        for entry in self.entrylist:
            entrystring = entrystring + entry.data +  " "  
        return entrystring

""" A DiaryEntry is stored as an object and it adds itself \
to the entry list """
class DiaryEntry:
    def __init__(self, entryList, data, currentTime=now):
        self.entryId = entryList.entryIndex
        self.created = "".join(str(now.day)+"/"+str(now.month)+"/"+str(now.year))
        self.modified = "".join(str(now.day)+"/"+str(now.month)+"/"+str(now.year))
        self.entryList = entryList
        self.data = data
        self.entryList.createEntry(self)

        
    def edit(self, entryContent, currentTime=now):
        """ this method edits diary entry's data """

        self.data = entryContent
        self. modified = currentTime
        self.entryList.modifyEntry(self)
        
    #def viewEntry(self):
        #entryDetails = ["entrydata: ", self.data, "... datecreated: " , \
                        #"".join(str(self.created.day)+"/"+str(self.created.month)\
                        #+"/"+str(self.created.year))]
        #return "".join(entryDetails)


def main():
    mydiaryobject = MyDiary()
    gordonbalaaka = User("Gordon Balaaka", "balaakagordon@gmail.com", "password", mydiaryobject)
    seconduser = User("Peter Crouch", "petercrouch@gmail.com", "password", mydiaryobject)
    jamesbond = User("James Bond", "007.amesbond@gmail.com", "bondjamesbond", mydiaryobject)   
    mydiaryobject.login("balaakagordon@gmail.com","password")
    entry1 = DiaryEntry(entryList=mydiaryobject.userEntries, data='this is my first entry', currentTime=now)
    entry2 = DiaryEntry(entryList=mydiaryobject.userEntries, data='this is my second entry', currentTime=now)

if __name__ == '__main__':
    main()    