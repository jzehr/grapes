'''
this is just to parse the XML to grab all the viruses
at this point, these will be used as variables in the pipeline
'''



import os
import json
import argparse
import xml.etree.ElementTree as et
from collections import Counter


def name_fixer(string):
    new = []
    bad_chars = [" ",",",".","/","-","(",")",":","'"]
    def checker(char):
        if char in bad_chars:
            return "_"
        else:
            return char
    for char in list(string):
        new.append(checker(char))

    temp = "".join(new)
    name = temp.replace("__","_")
    return name

def get_virus(elem):
    master = {}

    acc_num = name_fixer(str(elem.find("INSDSeq_accession-version").text))

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

    master[acc_num] = checker(get_qual("organism"))

    return master


parser = argparse.ArgumentParser()
parser.add_argument("--file", help="path to your rsrc XML file", type=str)
args = parser.parse_args()


in_file = args.file
#tree = et.parse("09-16-2019_grapevine.gbc.xml")
tree = et.parse(in_file)
root = tree.getroot()
temp_info = list(map(get_virus, root.findall("INSDSeq")))

info = {}
for i in temp_info:
    info.update(i)

temp = info.values()
temp = [i for j in temp for i in j]
this = [name_fixer(t) for t in temp]
payload = list(Counter(this))

file_name = "../data/all_viruses.txt"
print("Printing file to... ", file_name)
with open(file_name, "w") as out:
    for p in payload:
        out.write(p + "\n")












