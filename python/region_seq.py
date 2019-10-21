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
bads = {}
for r in regions:
    prods_in_region = []
    region_temp = {}
    countries = data[r]
    for key in acc_keys:
        target = name_fixer(info[key]["country"][0])
        if target in countries:
            prods = info[key]["product"]
            cds = info[key]["CDS"]

            if len(prods) != len(cds):
                print(info[key])

            else:

                '''
                this is where some data cleaning occurs
                '''
                for pos, item in enumerate(prods):
                    hsp70_like = ["heat_shock_70_like_protein", "heat_shock_protein_70_like_protein", "HSP70_like_protein", "Hsp70_like_protein", "heat_shock_protein_70_like_protein", "heat_schock_protein_70_like_protein"]
                    hsp70_h = ["heat_shock_protein_70_homologue", "HSP70h", "heat_shock_protein_hsp70h", "Heat_shock_protein_70_homolog"]
                    hsp90_like = ["Hsp90_like_protein","HSP90_like_protein"]
                    hsp90_h = ["heat_shock_protein_90_homologue", "HSP90h", "heat_shock_protein_hsp90h", "Heat_shock_protein_90_homolog"]

                    if name_fixer(item) in hsp70_like:
                        prods_in_region.append("hsp70_like")
                    elif name_fixer(item) in hsp70_h:
                        prods_in_region.append("hsp70_h")
                    elif name_fixer(item) in hsp90_like:
                        prods_in_region.append("hsp90_like")
                    elif name_fixer(item) in hsp90_h:
                        prods_in_region.append("hsp90_h")
                    else:
                        prods_in_region.append(name_fixer(item))

    region_prods = Counter(prods_in_region)
    good = []
    bad = []
    for i in list(region_prods.most_common()):
        if i[1] > 1:
            good.append(i[0])
        else:
            bad.append(i[0])

    if len(bad) == 0:
        bad.append("all_good")

    good_region = {}
    bad_region = {}

    good_region[r] = good
    bad_region[r] = bad
    master.update(good_region)
    bads.update(bad_region)

with open("data/TOO_FEW_PRODS.json", "w") as jf:
    json.dump(bads, jf, indent=3)

with open("data/GOOD_PRODS.json", "w") as jf:
    json.dump(master, jf, indent=3)

'''
now that we have the info we can make fasta files
'''
for r in regions:
    for prod in master[r]:
        fasta_out = "data/fasta/%s_%s.fasta" % (r, prod)
        with open(fasta_out, "w") as out:
            countries = data[r]
            for key in acc_keys:
                target = name_fixer(info[key]["country"][0])
                if target in countries:
                    prods = info[key]["product"]
                    cds = info[key]["CDS"]

                    if len(prods) != len(cds):
                        print(info[key])

                    else:

                        for pos, item in enumerate(prods):
                            hsp70_like = ["heat_shock_70_like_protein", "heat_shock_protein_70_like_protein", "HSP70_like_protein", "Hsp70_like_protein", "heat_shock_protein_70_like_protein", "heat_schock_protein_70_like_protein"]
                            hsp70_h = ["heat_shock_protein_70_homologue", "HSP70h", "heat_shock_protein_hsp70h", "Heat_shock_protein_70_homolog"]
                            hsp90_like = ["Hsp90_like_protein","HSP90_like_protein"]
                            hsp90_h = ["heat_shock_protein_90_homologue", "HSP90h", "heat_shock_protein_hsp90h", "Heat_shock_protein_90_homolog"]

                            if name_fixer(item) in hsp70_like:
                                item = "hsp70_like"
                            elif name_fixer(item) in hsp70_h:
                                item = "hsp70_h"
                            elif name_fixer(item) in hsp90_like:
                                item = "hsp90_like"
                            elif name_fixer(item) in hsp90_h:
                                item = "hsp90_h"
                            else:
                                item = name_fixer(item)

                            if item == prod:
                                results = write_fasta(info, key, pos, item)
                                header, seq, row = results[0], results[1], results[2]
                                out.write(">{}\n{}\n".format(header, seq))
