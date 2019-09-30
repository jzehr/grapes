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
        for i in checker(get_qual("product")):
            if i in good:
                #print("found one!!")
                data["country"] = checker(get_qual("country"))
        
                #print(master)
                return master
    

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to your rsrc XML file", type=str)
args = parser.parse_args()
in_file = args.file

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
this = [name_fixer(t) for t in temp]
counter = Counter(this)
payload = list(sorted(counter.items()))

file_name = "../data/csv/GLRaV3_countries.csv"
print("Writing all Countries and their frequencies associated with GLRaV3 and CP alphabetically to --> ", file_name)
with open(file_name, "w") as out:
    writer = csv.writer(out)
    header = ["country","freq"]
    writer.writerow(header)
    for p in payload:
        row = [p[0], p[1]]
        writer.writerow(row)


