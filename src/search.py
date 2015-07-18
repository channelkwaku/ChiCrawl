from math import radians, cos, sin, asin, sqrt
import sqlite3
import json
import re
import os

#query the database
def search(args, lat, lon):
    if not args:
        return []
    connection = sqlite3.connect('data/bars.db')
    connection.create_function("distance", 4, distance_between)
    c = connection.cursor()

    s = 'SELECT name, longitude, latitude, weighted_rank, distance(' + str(lon) + ', ' + str(lat) + ', longitude, latitude) AS walking_distance FROM bars WHERE walking_distance < ? GROUP BY name'

    bars = c.execute(s, (args.get('distance'),)).fetchall()
    return sort_bars_by_wr(bars)

#Haversine equation
def distance_between(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    lon_dist = lon2-lon1
    lat_dist = lat2-lat1
    a = sin(lat_dist/2)**2 + cos(lat1)*cos(lat2)*sin(lon_dist/2)**2
    c = 2*asin(sqrt(a))

    km = 6367*c
    mile = km*0.621371
    return mile

#reorganize list of bars by weighted rank
def sort_bars_by_wr(bars):
    ranked_bars = sorted(bars, key=lambda tup: tup[3], reverse=True)
    return ranked_bars

'''
if __name__ == "__main__":
    args = {'neighbor': 'Lincoln Park', 'distance': 2} 
    #args = [41.9075, -87.6769, 1.0]
    lat = 41.9075
    lon = -87.6769
    print search(args, lat, lon)
'''

