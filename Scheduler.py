import pandas as pd;
import csv;
import time;
import random;
from datetime import date;

s = open('Schedule.txt', 'w')
schedule = open("Schedule.xlsx", 'w')
log = open("Log.txt", 'w')
csvfile = open("Copy of Photographer_Availability_May_2025.csv")
reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)

# This program reads CSV files containing photographer availability and a list of events, and assigns photographers to events based on their availability and experience level.

# Populate lists of available photographers in each location, then sort and write lists to schedule file
def populate_lists(date, loop_reader):
    main_list = []
    penn_list = []
    srb_list = []
    ctma_list = []
    main_event_list = []
    penn_event_list = []
    srb_event_list = []
    ctma_event_list = []
    
    for row in loop_reader:
            if (row[0] == "Photographer") or (row[0] == "") or (row[date] == "TRUE"):
                continue
            if location_toggle(row[0]) == 0:
                if row[1] == "":
                    row[1] = random.randint(1,4) # for testing purposes, assign experience level to any photographer without one
                if isinstance(row[1], str):
                    row[1] = int(row[1])
                photographer = (row[0], row[1])
                match location_id:
                    case 0:
                        main_list.append(photographer)
                    case 1:
                        penn_list.append(photographer)
                    case 2:
                        srb_list.append(photographer)
                    case 3:
                        ctma_list.append(photographer)
    sort_lists(main_list, penn_list, srb_list, ctma_list)
    write_lists(main_list, penn_list, srb_list, ctma_list)

# Populate the schedule file with list of available photographers for each date
def populate_date():

    global location_id
    date_idx = 2
    csvfile.seek(0)
    next(reader)
    second_row = next(reader)
    
    # Calculate number of iterations based on the number of dates
    d1 = second_row[2]
    d2 = second_row[-1]
    m1 = d1.split("/")
    m2 = d2.split("/")
    date1 = date(date.today().year, int(m1[0]), int(m1[1]))
    date2 = date(date.today().year, int(m2[0]), int(m2[1]))
    diff = date2 - date1
    days = diff.days

    while date_idx <= (days + 2): # Account for the first two columns in the CSV
        s.write("\n")
        s.write(f"Date: {second_row[date_idx]}\n")
        csvfile.seek(0)
        loop_reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
        next(loop_reader)
        populate_lists(date_idx, loop_reader)
        date_idx += 1
        location_id = 0

# Helper function purgatory

# Toggle which list is being populated based on current location
# return 1 when changing location, otherwise return 0
location_id = 0
def location_toggle(location):
        global location_id
        match location:
            case "Pennsylvania":
                location_id = 1
                return 1
            case "Syracuse / Rochester / Buffalo":
                location_id = 2
                return 1
            case "CT / MA":
                location_id = 3
                return 1
            case _:
                return 0

# Arrange lists of photographers by experience level in descending order
def sort_lists(main_list, penn_list, srb_list, ctma_list):
    main_list.sort(key=lambda x: x[1], reverse=True)
    penn_list.sort(key=lambda x: x[1], reverse=True)
    srb_list.sort(key=lambda x: x[1], reverse=True)
    ctma_list.sort(key=lambda x: x[1], reverse=True)

# Write lists of available photographers on the specified date to the schedule file
def write_lists(main_list, penn_list, srb_list, ctma_list):
    s.write("Main List: \n" + "".join(str(i) for i in main_list))
    s.write("\n")
    s.write("Pennsylvania List: \n" + "".join(str(i) for i in penn_list))
    s.write("\n")
    s.write("Syracuse / Rochester / Buffalo List: \n" + "".join(str(i) for i in srb_list))
    s.write("\n")
    s.write("CT / MA List: \n" + "".join(str(i) for i in ctma_list))
    s.write("\n")

# Commands to be executed at runtime
populate_date()