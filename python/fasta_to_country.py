import json
import csv
import re

from python.helper import name_fixer
from python.helper import write_fasta



def country_fasta(in_file, out_fasta, countries):
    in_f = str(in_file)
    out_fas = out_fasta 
    countries = countries

    with open(in_f) as json_f:
        data = json.load(json_f)
        keys = list(data.keys())
        good = ["35 kDa coat protein", "major coat protein", "CP", "coat protein"]
        for num, country in enumerate(countries):
            print(country)
            with open(out_fas[num], "w") as out_fasta:
                print("writing this fasta --> ", out_fas[num])
                for p in keys:
                    prods = data[p]["product"]

                    this_c = name_fixer(data[p]["country"][0])
                    that_c = name_fixer(country)
                    
                    for pos, item in enumerate(prods):
                        if item in good and that_c == this_c:
                            results = write_fasta(data, p, pos, item)
                            header, seq, row = results[0], results[1], results[2]
                            out_fasta.write(">{}\n{}\n".format(header,seq))
                        else:
                            continue
                            

