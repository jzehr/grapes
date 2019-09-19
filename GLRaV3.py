import json
import re

## get it for GPGV, GVA, and GLRaV3 ##
files = ["data/Grapevine_leafroll_associated_virus_3.json", "data/Grapevine_virus_A.json", "data/Grapevine_Pinot_gris_virus.json"]
#files = ["data/Grapevine_leafroll_associated_virus_3.json"]



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
    name = temp.replace("__", "_")
    return name

def cds_fixer():
    pass


for file in files:
    with open(file) as json_f:
        new_fasta = file.split("/")[1].split(".")[0] + ".fasta"
        data = json.load(json_f)
        with open(new_fasta, "w") as out:
            good = ["35 kDa coat protein", "major coat protein", "CP", "coat protein"]
            keys = list(data.keys())
            #print(keys)
            for p in keys:
                prods = data[p]["product"]
                for pos, item in enumerate(prods):
                    if item in good:
                        print("found one!")
                        acc_num = p
                        print(acc_num)
                        CDS = data[p]["CDS"][pos]
                        orf1_s, orf1_e = int(re.findall(r'\d+', CDS.split("..")[0])[0]) - 1, int(re.findall(r'\d+', CDS.split("..")[1])[0])

                        print("this is CDS ", orf1_s, orf1_e)

                        if data[p]["collection_date"][0] == "no_value":
                            date = data[p]["create_date"]
                        else:
                            date = data[p]["collection_date"][0]
                        print(name_fixer(date))
                        country = data[p]["country"][0]
                        print(name_fixer(country))
                        host = data[p]["host"][0]
                        print(name_fixer(host))
                        strain = data[p]["strain"][0]
                        print(name_fixer(strain))
                        isolate = data[p]["isolate"][0]
                        print(name_fixer(isolate))

                        ## grab the full sequence ##
                        nuc_seq = data[p]["nuc_seq"]
                        seq = nuc_seq[orf1_s:orf1_e]

                        ## write the instance you have found ##
                        header = "%s_%s_%s_%s_%s_%s_%s" % (name_fixer(acc_num), name_fixer(item), name_fixer(date), name_fixer(country), name_fixer(host), name_fixer(strain), name_fixer(isolate))
                        header = header.replace("__","_")
                        out.write(">{}\n{}\n".format(header,seq))

                    else:
                        continue
