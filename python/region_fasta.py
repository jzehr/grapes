import json
import csv
from collections import Counter
import re

from python.helper import name_fixer
from python.helper import write_fasta

def region_fasta(input_j, output_fas, output_csv, region, product, data_dict):
    #print(f"in_f {input_j}, out_fas {output_fas}, out_csv {output_csv}, region {region}")

    in_j = str(input_j)

    out_fas = str(output_fas)
    out_csv = str(output_csv)

    region = region
    product = product

    areas = data_dict[region]

    CPs = ["35 kDa coat protein", "major coat protein", "CP", "coat protein"]

    with open(in_j) as json_f:
        data = json.load(json_f)

    region_results = list(filter(lambda x: name_fixer(data[x]["country"]) in areas, data))
    #print(region_results)


    temp_prods = [data[r]["product"] for r in region_results if name_fixer(data[r]["product"]) == product]
    prods = list(Counter([name_fixer(i) for j in temp_prods for i in j]))
    print(f"This is the region {region} and here are the products {prods}")

    '''
    for p in prods:
        with open(output_fas, "w") as out:



    if product in CPs:
        with open(output_fas, "w") as out:
            for key in region_results:
                prods = data[p]["product"]


    else:
        break
    '''









