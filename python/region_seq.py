import json
import argparse
import xml.etree.ElementTree as et
from collections import Counter
import re

from helper import name_fixer, element_item, write_fasta


parser = argparse.ArgumentParser()
parser.add_argument("-x", "--xml_file", help="path to your rsrc XML file", type=str)
parser.add_argument("-j", "--json_file", help="path to your rsrc country JSON file", type=str)

args = parser.parse_args()

xml_file = args.xml_file
json_file = args.json_file

with open(json_file) as json_f:
    data = json.load(json_f)

tree = et.parse(xml_file)
root = tree.getroot()
temp_info = list(map(element_item, root.findall("INSDSeq")))

info = {}
errors = {}
for i in temp_info:

    ## grabbing master ##
    if type(list(i.keys())[0]) == str:
        if i is not None:
            info.update(i)

    ## grabbing errors ##
    else:
        temp = {}
        key = list(i.keys())[0][1]
        temp[key] = list(i.values())[0]
        errors.update(temp)


## 29 total seqs that are whacky... writing to separate file ##
#print(len(list(errors.keys())))

'''
## this is a sanity check to make sure no "bad values" are still in the master dict ##
for i in info:
    if info[i]["CDS"] == info[i]["product"]:
        print(info[i])
'''

with open("data/ACC_NUM_errors.json", "w") as jf:
    json.dump(errors, jf, indent=3)


acc_keys = list(info.keys())
regions = list(data.keys())

'''
scraping through the info dict to write each product sequence to a fasta file
'''

# making reference from one of our entries ##
# rather arbitrary at this point, can hard code later #
# assumes that there is one complete genome in the data #
genomes = {}
for i in info:
    if "genome" in info[i]["viral_source"]:
        temp = {}
        temp[i] = info[i]
        genomes.update(temp)

with open("data/COMPLETE_GENOMES.json", "w") as jf:
    json.dump(genomes, jf, indent=3)



master = {}
for r in regions:
    file_name = "data/fasta/%s_all.fasta" % r
    with open(file_name, "w") as out:
        temp = {}
        temp_prods = []
        countries = data[r]
        for key in acc_keys:
            target = name_fixer(info[key]["country"][0])
            if target in countries:
                prods = info[key]["product"]
                temp_prods.append(prods)
                cds = info[key]["CDS"]

                if len(prods) != len(cds):
                    print(info[key])

                else:

                    for pos, item in enumerate(prods):
                        results = write_fasta(info, key, pos, item)
                        header, seq, row = results[0], results[1], results[2]
                        out.write(">{}\n{}\n".format(header,seq))



        prods = [name_fixer(i) for j in temp_prods for i in j]
        counter_prods = Counter(prods)
        most = list(counter_prods.most_common())

        temp[r] = most
        master.update(temp)


