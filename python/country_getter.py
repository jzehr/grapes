'''
this is just to parse the XML to grab all of the unique countries in the XML,
and ALSO to grab the unique countries relating to GLRaV3
'''

import os
import json
import csv
import argparse
import xml.etree.ElementTree as et
from collections import Counter
import math
from opencage.geocoder import OpenCageGeocode

from helper import name_fixer


def get_country(elem):
    master = {}
    data = {}
    acc_num = name_fixer(str(elem.find("INSDSeq_accession-version").text))
    master[acc_num] = data

    def checker(lst):
        temp = lst
        if len(temp) == 0:
            temp.append("no_value")
        return temp

    def get_qual(word):
        temp = list(elem.iter("INSDQualifier"))
        temp_word = filter(lambda x: x.find("INSDQualifier_name").text == word, temp)
        new_word = list(map(lambda x: x.find("INSDQualifier_value").text, temp_word))
        return new_word

    good = ["35 kDa coat protein", "major coat protein", "CP", "coat protein"]
    #print(checker(get_qual("organism"))[0])

    if checker(get_qual("organism"))[0] == "Grapevine leafroll-associated virus 3":
        ''' we now want more than just the CP gene, so grabbing it all
        for i in checker(get_qual("product")):
            if i in good:
                #print("found one!!")
        '''
        data["country"] = checker(get_qual("country"))

                #print(master)
        return master

## pass in two tuples (coords) and get the distance between them ##
def distance(location_1, location_2):
    lat1, lon1 = location_1
    lat2, lon2 = location_2
    radius = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

## arg parse section ##
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to your rsrc XML file", type=str)
args = parser.parse_args()
in_file = args.file

## data that will stay constant ##
REGIONS = {
        "EUROPE": {
            "Spain": (39.3262345, -4.8380649),
            "Norway": (64.5731537, 11.5280364),
            "Ukraine": (49.4871968, 31.2718321),
            "Greece": (38.9953683, 21.9877132)},
        "SOUTH AMERICA": {
            "Brazil": (-10.3333333, -53.2),
            "Chile": (-31.7613365, -71.3187697 ),
            "Colombia": (2.8894434, -73.783892)},
        "NORTH AMERICA": {
            "Washington": (38.8948932, -77.0365529),
            "California": (36.7014631, -118.7559974),
            "New York": (40.7127281, -74.0060152),
            "Florida": (27.7567667, -81.4639835)},
        "MIDDLE EAST": {
            "Saudi Arabia": (25.6242618 , 42.3528328),
            "Syria": (34.6401861, 39.0494106),
            "Iran": (32.6475314 , 54.5643516),
            "Turkey": (38.9597594, 34.9249653)},
        "NORTH AFRICA": {
            "Algeria": (28.0000272, 2.9999825),
            "Niger": (17.7356214, 9.3238432),
            "Sudan": (15.4537439, 29.7951525),
            "Egypt": (26.2540493, 29.2675469)},
        "SOUTH AFRICA": {
            "Western Cape": (-33.546977, 20.72753),
            "South Africa": (-28.8166236, 24.991639),
            "Nambia": (4.193367, 28.7653709)},
        "ASIA": {
            "China": (35.000074, 104.999927),
            "South Korea": (36.5581914, 127.9408564),
            "India": (22.3511148, 78.6677428),
            "Russia": (64.6863136, 97.7453061)},
        "OCEANIA": {
            "Australia": (-24.7761086, 134.755 ),
            "New Zealand": (-41.5000831 , 172.8344077)}
            }


## getting tree object and parsing ##
tree = et.parse(in_file)
root = tree.getroot()
temp_info = list(map(get_country, root.findall("INSDSeq")))
info = {}
for i in temp_info:
    #print(i)
    if i is not None:
        info.update(i)
temp = list(info.values())
temp = [t["country"] for t in temp]
temp = [i for j in temp for i in j]
#this = [name_fixer(t) for t in temp]
#counter = Counter(this)
counter = Counter(temp)
payload = list(sorted(counter.items()))

locations = [pa[0] for pa in payload]


## opencage 2500 reqs per day##
## api key ##
key = "d8206078d64d423bbd9d85fd3d79cd8c"
geocoder = OpenCageGeocode(key)

info = []
for location in locations:
    all_ds = []
    if location != "no_value":
        print(location)
        results = geocoder.geocode(location)
        local = (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
        for key in REGIONS:
            country_dict = REGIONS[key]
            keys = list(country_dict.keys())
            #print(key)
            temp_distance = []
            for val in keys:
                temp_distance.append(distance(local, country_dict[val]))
            smallest = sum(temp_distance)/len(temp_distance)
            all_ds.append(smallest)
            #print(f"This is the avg distance from {location} to {key} --> {smallest}")
            #print("\n")

        zipped = list(zip(all_ds, list(REGIONS.keys())))
        m = min(zipped)
        info.append((location, m[1]))
        #print(f"{location} is closest to --> {m}")

#print(info)

master = {}
for r in REGIONS:
    temp = {}
    t = []
    for i in info:
        if i[1] == r:
            t.append(name_fixer(i[0]))
    temp[name_fixer(r)] = t
    master.update(temp)


file_name_json = "rsrc/GLRaV3_regions.json"
print("Writing all countries to regions for the json file --> ", file_name_json)
with open(file_name_json, "w") as out_file:
    json.dump(master, out_file, indent=2)

file_name_csv = "rsrc/GLRaV3_countries.csv"
print("Writing all Countries and their frequencies associated with GLRaV3 and CP alphabetically to --> ", file_name_csv)
with open(file_name_csv, "w") as out:
    writer = csv.writer(out)
    header = ["country","freq"]
    writer.writerow(header)
    for p in payload:
        row = [name_fixer(p[0]), p[1]]
        writer.writerow(row)


