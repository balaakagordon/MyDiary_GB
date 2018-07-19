# -*- coding: utf-8 -*-

#importing packages 
import datetime
from random import randrange
now = datetime.datetime.now()


class MyDiary:
    def __init__(self):
        self.userlist = {}
        self.currentUser = None
        self.userEntries = None
    
    def addUser(self, user):
        if user in list(self.userlist.values()): 
            return "User already exists"
        else:
            self.userlist[user.email] = user
        
    def login(self, loginEmail, loginPassword):
        if self.userlist[loginEmail].password == loginPassword:
            self.currentUser = self.userlist.get(loginEmail)
            self.userEntries = self.currentUser.entries
        else:
            print("incorrect login credentials")
    
    def logout(self):
        if self.currentUser != None:
            self.currentUser = None
            self.userEntries = None
        else:
            print("Nobody logged in!")


class User:
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
    def __init__(self):
        self.entrylist = []
        self.allEntries = None
        self.deletedEntries = None
        self.currentEntries = None
        
    def createEntry(self, DiaryEntry, entryId=len(mydiaryobject.entries.entrylist[-1])+1, mydiaryobject=mydiaryobject, currentTime=now):
        self.entrylist.append(DiaryEntry)
        
    def modifyEntry(self, DiaryEntry):
        for i in range(len(self.entrylist)-1):
            if self.entrylist[i].entryId == DiaryEntry.entryId:
                self.entrylist[i]=DiaryEntry 
    
    def deleteEntry(self, DiaryEntry):
        if DiaryEntry in list(self.entrylist.getvalues()):
            self.entrylist.pop(DiaryEntry.entryId)
    
    def __str__(self):
        entrystring = ""
        for entry in self.entrylist:
            entrystring = entrystring + entry.data +  " "  
        return entrystring


class DiaryEntry:
    def __init__(self, entryList, entryId, currentTime=now):
        self.entryId = randrange(1000, 9999, 1)
        self.entryId = entryId
        self.created = currentTime
        self.modified = currentTime
        self.entryList = entryList
        self.data = "this is diary entry number "+self.entryId+"."
        #self.data = raw_input("Please write your thought here:")
        self.entryList.createEntry(self)
        
    def edit(self, entryContent, currentTime=now):
        self.data = entryContent
        self. modified = currentTime
        self.entryList.modifyEntry(self)
        
    def viewEntry(self):
        entryDetails = ["content: ", self.data, "... date created: " , \
                        "".join(str(self.created.day)+"/"+str(self.created.month)\
                        +"/"+str(self.created.year))]
        return "".join(entryDetails)


def main():
    mydiaryobject = MyDiary()
    gordonbalaaka = User("Gordon Balaaka","balaakagordon@gmail.com","password",mydiaryobject)
    seconduser = User("Peter Crouch","petercrouch@gmail.com","password",mydiaryobject)
    jamesbond = User("James Bond","007.amesbond@gmail.com","bondjamesbond",mydiaryobject)   
    mydiaryobject.login("balaakagordon@gmail.com","password")
    entry1 = DiaryEntry(mydiaryobject.userEntries)
    entry2 = DiaryEntry(mydiaryobject.userEntries)

if __name__ == '__main__':
    main()    