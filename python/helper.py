import re


def name_fixer(string):
    new = []
    bad_chars = [" ",",",".","/","-","(",")",":","'", ";"]
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


def write_fasta(data, p, pos, item):
    #print(p, pos, item)
    acc_num = p
    CDS = data[p]["CDS"][pos]
    orf1_s, orf1_e = int(re.findall(r'\d+', CDS.split("..")[0])[0]) - 1, int(re.findall(r'\d+', CDS.split("..")[1])[0])
    if data[p]["collection_date"][0] == "no_value":
        date = data[p]["create_date"] 
    else:
        date = data[p]["collection_date"][0]
    country = data[p]["country"][0]
    host = data[p]["host"][0]
    strain = data[p]["strain"][0]
    isolate = data[p]["isolate"][0]
    nuc_seq = data[p]["nuc_seq"] 
    seq = nuc_seq[orf1_s:orf1_e]

    header = "%s_%s_%s_%s_%s_%s_%s" % (name_fixer(acc_num), name_fixer(item), name_fixer(date), name_fixer(country), name_fixer(host), name_fixer(strain), name_fixer(isolate))
    header = header.replace("__","_")
    row = (name_fixer(acc_num), name_fixer(item), name_fixer(date), name_fixer(country), name_fixer(host), name_fixer(strain), name_fixer(isolate))
    return header, seq, row






