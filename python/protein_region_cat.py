import subprocess
import json
import argparse
from collections import Counter

from flat import flatten

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to your GOOD_PRODS.json", type=str)
args = parser.parse_args()

in_file = args.file


def cat_files(prod, files):
    #print(f"catting this --> {prod} for --> {files}\n")

    regions = "_".join(files)
    cat_file = "data/fasta/cat_%s_%s.fasta" % (str(prod), regions)
    subprocess.call("touch %s" % cat_file, shell=True)
    subprocess.call("cat data/fasta/*%s.fasta > %s" % (prod, cat_file), shell=True)
    print(f"Done catting all {prod}s.")

with open(in_file) as j_file:
    data = json.load(j_file)

keys = list(data.keys())

all_prods = [data[key] for key in keys]
all_prods = Counter(flatten(all_prods))

## if you have more than 1 entry, lets cat you with the regions ##
goods = {key: value for key, value in all_prods.items() if value > 1}
good_keys = list(goods.keys())

cats = {}
for gk in good_keys:
    temp = {}
    regions = []
    for key in keys:
        prods = data[key]
        if gk in prods:
            regions.append(key)

    temp[gk] = regions
    cats.update(temp)

for key, value in cats.items():
    cat_files(key, value)

with open("data/CAT_REGION_PRODS.json", "w") as out_file:
    json.dump(cats, out_file, indent=2)





