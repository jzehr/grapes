import csv
import json
import argparse
import xml.etree.ElementTree as et

from collections import Counter

from helper import element_item, name_fixer



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to your rsrc XML file", type=str)
args = parser.parse_args()

in_file = args.file

tree = et.parse(in_file)
root = tree.getroot()
temp_info = list(map(element_item, root.findall("INSDSeq")))
info = {}
for i in temp_info:
    if i is not None:
        info.update(i)

'''
for key, value in info.items():
    print(f"{key} | {value}\n")
'''


with open("rsrc/GLRaV3_data.json", "w") as out_j:
    json.dump(info, out_j, indent=2)

