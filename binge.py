#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt 
import datetime
import scipy.optimize as opt;
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from scipy.interpolate import interp1d

def read_data_from_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
        data = data[1:]
    return data

def estimate_time(name):
    if "Staffel" in name:
        if "Big Bang" in name or "Family Guy" in name or "Brooklyn Nine-Nine" in name or "New Girl" in name or "How I Met" in name or "Rick and Morty" in name:
            return 0.2
        else:
            return 0.45
    else:
        return 1.5

def get_list_of_dates(start,end):
    dates = []
    delta = end - start
    for i in range(delta.days + 1):
        dates.append(start + datetime.timedelta(days=i))
    return dates

data = read_data_from_file('NetflixViewingHistory.csv')
calendar = get_list_of_dates(datetime.datetime(2015, 6, 1,0,0,0),datetime.datetime.now())
#calendar = get_list_of_dates(datetime.datetime(2016, 10, 7,0,0,0),datetime.datetime.now())

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
            all_episodes.append(int(episodes[i]))
    if not found:
        all_episodes.append(int(0))

compress_days = 14
dates_compressed = []
episodes_compressed = []
i = 0
while i+compress_days < len(calendar):
    print("i is " + str(i) + " handling dates " + str(calendar[i]) + " to " + str(calendar[i+compress_days]))
    dates_compressed.append(calendar[i])
    value = 0
    for y in range(compress_days-1):
        value += all_episodes[i+y]
    episodes_compressed.append(value)
    i += compress_days

for x in range(len(episodes_compressed)):
    print(str(x) + ": " + str(dates_compressed[x]) + ": " + str(episodes_compressed[x]))

stacked_consume = []
for i in range(len(dates_compressed)):
    stacked_value = 0
    for k in range(i):
        stacked_value += episodes_compressed[k]
    stacked_consume.append(stacked_value)

date_number_array = range(0,len(episodes_compressed))

x=np.array(date_number_array)
y=np.array(episodes_compressed)

x_new = np.linspace(x.min(), x.max(),500)

f = interp1d(x, y, kind='quadratic')
y_smooth=f(x_new)

plt.title('Netflix Stats smoothed')
plt.plot(x_new,y_smooth)
#plt.scatter (x, y)
plt.show()

#plt.style.use('ggplot')
#plt.plot(dates_compressed, ysmoothed)

#plt.bar(dates_compressed, ysmoothed,40)

plt.plot(dates_compressed, stacked_consume)
#plt.xlabel('Datum') 
#plt.ylabel('Konsum') 
plt.title('Netflix Stats Stacked') 
plt.show() 