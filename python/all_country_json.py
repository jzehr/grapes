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

from helper import element_item, name_fixer, distance

## arg parse section ##
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to your rsrc XML file", type=str)
parser.add_argument("-l", "--locations", help="path to your locations json", type=str)
args = parser.parse_args()
in_file = args.file
locations_file = args.locations

## getting tree object and parsing ##
tree = et.parse(in_file)
root = tree.getroot()
temp_info = list(map(element_item, root.findall("INSDSeq")))
info = {}
for i in temp_info:
    if i is not None:
        info.update(i)

## making two dicts to house good data
## and one with errors in it
good_info = {}
error_info = {}
for key, value in info.items():
    if type(key) != tuple:
        temp = {}
        temp[key] = value
        good_info.update(temp)
    else:
        temp = {}
        temp[key[1]] = value
        error_info.update(temp)



with open("rsrc/good_info.json", "w") as j_out:
    json.dump(good_info, j_out, indent=2)


with open("rsrc/error_info.json", "w") as j_out:
    json.dump(error_info, j_out, indent=2)


temp = list(info.values())
temp_country = [t["country"] for t in temp]
country = [i for j in temp_country for i in j]
counter_country = Counter(country)

'''
temp_prods = [t["product"] for t in temp]
prods = [i for j in temp_prods for i in j]
counter_prods = Counter(prods)

payload = list(sorted(counter_country.items()))
locations = [pa[0] for pa in payload]

## opencage 2500 reqs per day##
## api key ##
key = "d8206078d64d423bbd9d85fd3d79cd8c"
geocoder = OpenCageGeocode(key)

with open(locations_file) as json_in:
    REGIONS = json.load(json_in)

info = []
for location in locations:
    all_ds = []
    if location != "no_value":
        print(f"location: {location}")
        if ":" in location:
            results = geocoder.geocode(location.split(":")[0])
        else:
            results = geocoder.geocode(location)
        local = (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
        for key in REGIONS:
            country_dict = REGIONS[key]
            keys = list(country_dict.keys())
            #print(f"comparing to this key from REGIONDS: {key}")
            temp_distance = []
            for val in keys:
                temp_distance.append(distance(local, country_dict[val]))
            smallest = sum(temp_distance)/len(temp_distance)
            all_ds.append(smallest)
            #print(f"This is the avg distance from {location} to {key} --> {smallest}")

        zipped = list(zip(all_ds, list(REGIONS.keys())))
        m = min(zipped)
        info.append((location, m[1]))

master = {}
for r in REGIONS:
    temp = {}
    t = []
    for i in info:
        if i[1] == r:
            t.append(name_fixer(i[0]))
    temp[name_fixer(r)] = t
    master.update(temp)

master["NV"] = ["no_value"]

file_name_json = "rsrc/GLRaV3_regions.json"
print("Writing all countries to regions for the json file --> ", file_name_json)
with open(file_name_json, "w") as out_file:
    json.dump(master, out_file, indent=2)

file_name_csv = "rsrc/GLRaV3_countries.csv"
#print("Writing all Countries and their frequencies associated with GLRaV3 and CP alphabetically to --> ", file_name_csv)
print("Writing all Countries and their frequencies associated with GLRaV3 alphabetically to --> ", file_name_csv)
with open(file_name_csv, "w") as out:
    writer = csv.writer(out)
    header = ["country","freq"]
    writer.writerow(header)
    for p in payload:
        row = [name_fixer(p[0]), p[1]]
        writer.writerow(row)
'''
