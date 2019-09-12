'''
this is just to parse the XML to grab all the viruses
at this point, these will be used as variables in the pipeline
'''



import os
import json
import xml.etree.ElementTree as et
from collections import Counter


def name_fixer(string):
    new = []
    bad_chars = [' ',',','.','/','-','(',')',':']
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


tree = et.parse("total_viral_sequences_09-05-19.gbc.xml")
root = tree.getroot()
temp_info = list(map(get_virus, root.findall("INSDSeq")))

info = {}
for i in temp_info:
    info.update(i)

temp = info.values()
temp = [i for j in temp for i in j]
this = [name_fixer(t) for t in temp]
payload = list(Counter(this))

file_name = "all_viruses.txt"
with open(file_name, "w") as out:
    for p in payload:
        out.write(p + "\n")












