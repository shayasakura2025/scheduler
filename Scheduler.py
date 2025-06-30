import pandas as pd;
import csv;

""" class Employee:
    def __init__(self, employeeName, employeeID, employeeHome, employeeLvl):
        self.employeeName = employeeName
        self.employeeID = employeeID
        self.employeeHome = employeeHome
        self.employeeLvl = employeeLvl

    def getName(self):
        return self.employeeName
    
    def getID(self):
        return self.employeeID
    
    def getHome(self):
        return self.employeeHome
    
    def getLvl(self):
        return self.employeeLvl """
    
""" class Event:
    def __init__(self, eventName, eventID, eventLocation, eventStart, EventEnd):
        self.eventName = eventName
        self.eventID = eventID
        self.eventLocation = eventLocation
        self.eventStart = eventStart
        self.eventEnd = EventEnd

    def getName(self):
        return self.eventName
    
    def getID(self):
        return self.eventID
    
    def getLocation(self):
        return self.eventLocation
    
    def getStart(self):
        return self.eventStart
    
    def getEnd(self):
        return self.eventEnd """
    
photographerList = []
idIndex = 0
with open("schedule.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
    for row in reader:
        photographerList.append(row)

    for row in photographerList:
        if row[1] == "":
            row[1] = idIndex
            idIndex += 1

eventList = []
eventIndex = 0
with open("events.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
    for row in reader:
        eventList.append(row)
    
    for row in eventList:
        if row[1] == "":
            row[1] = eventIndex
            eventIndex += 1

captainList = []
experiencedList = []
rookieList = []

for row in photographerList:
    if row[3] == "Captain":
        captainList.append(row)
    elif row[3] == "Experienced":
        experiencedList.append(row)
    elif row[3] == "Rookie":
        rookieList.append(row)
    else:
        print("Error: Invalid photographer level found in schedule.csv")

print(captainList)
print(experiencedList)
print(rookieList)