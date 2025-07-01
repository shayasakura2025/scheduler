import pandas as pd;
import csv;
import osmnx as ox;
import networkx as nx;
from geopy.geocoders import Nominatim;
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable;
import sklearn as sk;
import time;

s = open('Schedule.txt', 'w')
log = open("Log.txt", 'w')

photographerList = []
""" 
photographer index key 
name = 0
id = 1
address = 2
level = 3
start time = 4
end time = 5
days available = 6 through 12
"""
idIndex = 0
with open("Schedule - Photographers.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
    for row in reader:
        if row[0] != "Name":
            photographerList.append(row)

    for row in photographerList:
        if row[1] == "":
            row[1] = idIndex
            idIndex += 1
print(photographerList)

eventList = []
""" event index key
name = 0
id = 1
address = 2
start time = 3
end time = 4
photographers = 5
day of week = 6
"""
eventIndex = 0
with open("Schedule - Events.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
    for row in reader:
        if row[0] != "Name":
            eventList.append(row)
    
    for row in eventList:
        if row[1] == "":
            row[1] = eventIndex
            eventIndex += 1

captainList = []
experiencedList = []
rookieList = []

for row in photographerList:
    if row[6] == "Captain":
        captainList.append(row)
    elif row[6] == "Experienced":
        experiencedList.append(row)
    elif row[6] == "Rookie":
        rookieList.append(row)
    else:
        print("Error: Invalid photographer level found in schedule.csv")

print(captainList)
print(experiencedList)
print(rookieList)

app = Nominatim(user_agent="photographer_scheduler")

def getLocationByAddress(photographer):
        print(f"Geocoding address for photographer {photographer[0]} with ID {photographer[1]}")
        photographerAddress = []
        photographerAddress.append(photographer[2])
        photographerAddress.append(photographer[3])
        photographerAddress.append(photographer[4])
        photographerAddress.append(photographer[5])
        print(photographerAddress)
        str_address = ', '.join(photographerAddress)
        print(str_address)
        try:
            location = app.geocode(str_address)
        except (GeocoderTimedOut, GeocoderUnavailable):
            location = app.geocode(str_address)
        if location: 
            photographer[2] = f"{location.latitude},{location.longitude}"
            print (f"Geocoded address {photographer[2]} for photographer {photographer[0]}")
        else:
            print(f"Error: Could not geocode address {photographer[2]} for photographer {photographer[0]}")

def getEventLocationByAddress(event):
            print(f"Geocoding address for event {event[0]} with ID {event[1]}")
            eventAddress = []
            eventAddress.append(event[2])
            eventAddress.append(event[3])
            eventAddress.append(event[4])
            eventAddress.append(event[5])
            print(eventAddress)
            str_address = ', '.join(eventAddress)
            print(str_address)
            try:
                location = app.geocode(str_address)
            except (GeocoderTimedOut, GeocoderUnavailable):
                location = app.geocode(str_address)
            if location:
                event[2] = f"{location.latitude},{location.longitude}"
                print (f"Geocoded address {event[2]} for event {event[0]}")
            else:
                print(f"Error: Could not geocode address {event[2]} for event {event[0]}")               
    


def optimizePlacement():
    distList = []
    # Create a graph from the street network
    #G = ox.graph_from_bbox((39, -80, 48, -66), network_type='drive')
    G_tut = ox.graph_from_place('Worcester, Massachusetts, USA', network_type='drive', simplify = True)
    
    # Convert the graph to a directed graph
    #G = G.to_directed()
    G_tut = G_tut.to_directed()
    
    
    # Calculate the shortest path between each photographer's home and each event location
    for event in eventList:
        eventLocation = event[2]
        event_lat = float(eventLocation.split(",")[0])
        event_lon = float(eventLocation.split(",")[1])
        print (f"Event location: {event[0]} (X: {event_lat}, Y: {event_lon})")
        for photographer in photographerList:
            photographerAddress = photographer[2]
            photographer_lat = float(photographerAddress.split(",")[0])
            photographer_lon = float(photographerAddress.split(",")[1])
            print(f"Photographer location: {photographer[0]} (X: {photographer_lat}, Y: {photographer_lon})")
            if photographerAddress != "" and eventLocation != "":
                orig_node = ox.distance.nearest_nodes(G_tut, photographer_lon, photographer_lat)
                dest_node = ox.distance.nearest_nodes(G_tut, event_lon, event_lat)
                route = nx.shortest_path_length(G_tut, orig_node, dest_node, weight ='length')
                print(f"Shortest path from {photographerAddress} to {eventLocation}: {route}")
                log.write(f"Shortest path from {photographerAddress} to {eventLocation}: {route}\n")
                distList.append(photographer, event, route)
            else:
                print(f"No path found from {photographerAddress} to {eventLocation}")

for photographer in photographerList:
    getLocationByAddress(photographer)
for event in eventList:
    getEventLocationByAddress(event)
optimizePlacement()