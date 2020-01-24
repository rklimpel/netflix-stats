#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt 
import datetime

def estimate_time(name):
    if "Staffel" in name:
        if "Big Bang" in name or "Family Guy" in name or "Brooklyn Nine-Nine" in name or "New Girl" in name or "How I Met" in name or "Rick and Morty" in name:
            return 0.2
        else:
            return 0.45
    else:
        return 1.5

# Read data from csv file into data list
data = []
with open('NetflixViewingHistory.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)
    data = data[1:]

# split for data and episode count lists
dates = []
episodes = []
for log in data:
    if not dates:
        dates.append(log[1])
        episodes.append(1)
    else:
        if dates[-1] == log[1]:
            episodes[-1] += estimate_time(log[0])
        else:
            dates.append(log[1])        
            episodes.append(estimate_time(log[0]))

# Build a calendar of every date between start and end
start = datetime.datetime(2015, 6, 1,0,0,0)
end = datetime.datetime.now()
delta = end - start
calendar = []
for i in range(delta.days + 1):
    calendar.append(start + datetime.timedelta(days=i))

#Convert dates from csv to date objects
for i in range(len(dates)):
    objDate = datetime.datetime.strptime(dates[i], "%d.%m.%y")
    dates[i] = objDate

all_episodes = []
for day in calendar:
    found = False
    for i in range(len(dates)):
        if(dates[i] == day):
            found = True
            all_episodes.append(episodes[i])
    if not found:
        all_episodes.append(0)

#Compress the data 
compress_days = 7
dates_compressed = []
episodes_compressed = []
for i in range(len(dates)):
    dates_compressed.append(dates[i])
    value = 0
    for y in range(compress_days-1):
        value += all_episodes[i+y]
    episodes_compressed.append(value)
    i += compress_days

#stacked_consume = []
#for i in range(len(dates_compressed)):
#    stacked_value = 0
#    for k in range(i):
#        stacked_value += episodes_compressed[k]
#    stacked_consume.append(stacked_value)
    

plt.plot(dates_compressed, episodes_compressed)
#plt.plot(dates_compressed, stacked_consume)
plt.xlabel('Datum') 
plt.ylabel('Konsum') 
plt.title('Netflix Stats') 
plt.show() 