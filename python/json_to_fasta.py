import json
import csv
import re


from python.helper import name_fixer
from python.helper import write_fasta

def fasta_maker(in_file, out_fasta, out_csv):
    in_json_file = str(in_file)
    out_total_fas = str(out_fasta)
    out_total_csv = str(out_csv)
    
    with open(in_json_file) as json_f:
        data = json.load(json_f)
        with open(out_total_csv, "w") as csv_file, open(out_total_fas, "w") as out:
            writer = csv.writer(csv_file)
            row_header =  ["acc_num", "protein", "date", "country", "host", "strain", "isolate"]
            writer.writerow(row_header)
            good = ["35 kDa coat protein", "major coat protein", "CP", "coat protein"]
            keys = list(data.keys())

            ## writing all to a file if contain coat protein ##
            for p in keys:
                prods = data[p]["product"]
                for pos, item in enumerate(prods):
                    if item in good:
                        results = write_fasta(data, p, pos, item)
                        header, seq, row = results[0], results[1], results[2]
                        out.write(">{}\n{}\n".format(header,seq))
                        
                        writer.writerow(row)
                        
                    else:
                        continue
                    
