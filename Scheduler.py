import pandas as pd;
import csv;
import time, datetime;
import random;
from datetime import date;

s = open('Schedule.txt', 'w')
e = open("Events.txt", "w")
schedule = open("Schedule.xlsx", 'w')
log = open("Log.txt", 'w')
photographer_file = open("Copy of Photographer_Availability_May_2025.csv")
event_file = open("Copy of 2025 Graduation Schedule.csv", encoding="cp437")

# This program reads CSV files containing photographer availability and a list of events, and assigns photographers to events based on their availability and experience level.

# Populate lists of available photographers in each location, then sort and write lists to schedule file
main_list = []
penn_list = []
srb_list = []
ctma_list = []
def populate_photographer_lists(date, loop_reader):
    global main_list, penn_list, srb_list, ctma_list
    main_list = []
    penn_list = []
    srb_list = []
    ctma_list = []
    for row in loop_reader:
            if (row[0] == "Photographer") or (row[0] == "") or (row[date] == "TRUE"):
                continue
            if location_toggle(row[0]) == 0:
                if row[1] == "":
                    row[1] = random(1, 4) # for testing purposes, assign experience level to any photographer without one
                if isinstance(row[1], str):
                    row[1] = int(row[1])
                photographer = (row[0], row[1], "")
                match location_id:
                    case 0:
                        main_list.append(photographer)
                    case 1:
                        penn_list.append(photographer)
                    case 2:
                        srb_list.append(photographer)
                    case 3:
                        ctma_list.append(photographer)
    sort_photographers()
    write_lists(main_list, penn_list, srb_list, ctma_list)

main_event_list = []
penn_event_list = []
srb_event_list = []
ctma_event_list = []
def populate_event_lists(current_date, loop_reader):
    global main_event_list, penn_event_list, srb_event_list, ctma_event_list
    main_event_list = []
    penn_event_list = []
    srb_event_list = []
    ctma_event_list = []
    for row in loop_reader:
        date = row[0].split(" ")
        if date != [""]:
            date = date[1]
            date = date.split("/")
            date = date[0] + "/" + date[1]
        if current_date == date:
            captain = row[8].split(";")
            captain = captain[0]
            event = (row[1], row[4], row[5], row[7], captain)
            region = randomize_region()
            match region:
                case "Main":
                    main_event_list.append(event)
                case "Pennsylvania":
                    penn_event_list.append(event)  
                case "Syracuse / Rochester / Buffalo":
                    srb_event_list.append(event)
                case "CT / MA":
                    ctma_event_list.append(event)
    sort_events()
    write_lists(main_event_list, penn_event_list, srb_event_list, ctma_event_list)

def populate_events():
    # Populate events with photographers, prioritizing previous captains
    for event in main_event_list:
        e.write(str(event[0]) + "\n")
        event_staff = []
        start_time = datetime.datetime.strptime(event[1], "%I:%M %p")
        e.write(str(start_time) + "\n")
        run_time = event[2]
        staff_needed = event[3]
        previous_captain = event[4]
        for idx, photographer in enumerate(main_list):
            p_name = photographer[0]
            p_level = photographer[1]
            if photographer[2] != "":
                p_available = photographer[2]
            else:
                p_available = start_time
            captain = ""
            if (p_name == previous_captain) and (p_available <= start_time):
                captain = p_name
                break
            elif (p_level == 4) and (p_available <= start_time) and (captain == ""):
                captain = p_name
        event_staff.append(captain)
        buffer_time = datetime.timedelta(hours=6)
        p_updated = (p_name, p_level, start_time + buffer_time)
        main_list[idx] = p_updated
        #while (event_staff.len <= staff_needed - 1):
        e.write("".join(str(i) for i in event_staff) + "\n")

# Populate the schedule file with list of available photographers for each date
def populate_date():
    reader = csv.reader(photographer_file, quoting=csv.QUOTE_ALL)
    global location_id
    date_idx = 3
    photographer_file.seek(0)
    next(reader)
    second_row = next(reader)
    
    # Calculate number of iterations based on the number of dates
    d1 = second_row[3]
    d2 = second_row[-1]
    m1 = d1.split("/")
    m2 = d2.split("/")
    date1 = date(date.today().year, int(m1[0]), int(m1[1]))
    date2 = date(date.today().year, int(m2[0]), int(m2[1]))
    diff = date2 - date1
    days = diff.days

    while date_idx <= (days + 3): # Account for the first two columns in the CSV
        s.write("\n")
        s.write(f"Date: {second_row[date_idx]}\n")
        photographer_file.seek(0)
        photographer_reader = csv.reader(photographer_file, quoting=csv.QUOTE_ALL)
        next(photographer_reader)
        populate_photographer_lists(date_idx, photographer_reader)
        event_file.seek(0)
        event_reader = csv.reader(event_file, quoting=csv.QUOTE_ALL)
        next(event_reader)
        s.write("Events:\n")
        populate_event_lists(second_row[date_idx], event_reader)
        populate_events()
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
def sort_photographers():
    main_list.sort(key=lambda x: x[1], reverse=True)
    penn_list.sort(key=lambda x: x[1], reverse=True)
    srb_list.sort(key=lambda x: x[1], reverse=True)
    ctma_list.sort(key=lambda x: x[1], reverse=True)

def sort_events():
    main_event_list.sort(key=lambda x: x[1])
    penn_event_list.sort(key=lambda x: x[1])
    srb_event_list.sort(key=lambda x: x[1])
    ctma_event_list.sort(key=lambda x: x[1])

def randomize_region():
    # Randomly place event in one of the four regions, for testing purposes only
    region = random.randint(1, 4)
    match region:
        case 1:
            return "Pennsylvania"
        case 2:
            return "Syracuse / Rochester / Buffalo"
        case 3:
            return "CT / MA"
        case 4:
            return "Main"

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
    s.flush()

# Commands to be executed at runtime
populate_date()
s.close()