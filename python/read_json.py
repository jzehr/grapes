import json
from collections import Counter 

'''
1. should separate based on:
    "protein type"

2. then append country to the sequence header + the accession number

'''


def json_to_fasta(infile, virus):
    
    def name_fixer(count):
        temp = count.replace(' ', '_')
        t_t = temp.replace(',', '__')
        name = t_t.replace('/','__')
        return name

    file = infile
    # search_term = ''
    # if virus == 'GLRaV3':
    #     search_term = ''
    

    master_dict = {'GVA': ('Grapevine virus A', 'Grapevine virus A (GVA)'),\
                    'GLRaV3' :('Grapevine leafroll-associated virus 3 (GLRaV-3)','Grapevine leafroll-associated virus 3m'),\
                     'GPGV' :('Grapevine Pinot gris virus','Grapevine Pinot gris virus')} 

    search_term = master_dict[virus]

    acc_num = []
    products = []
    source = []
    country = []
    seq = []
    host = []
    date = []
    with open(file) as infile:
        data = json.load(infile)
        for p in data.items():
            virus_source = p[1]['source'] 
            if virus_source == search_term[0] or virus_source == search_term[1]:
                acc_num.append(p[0])
                products.append(p[1]['product'])
                source.append(p[1]['source'])
                country.append(p[1]['country'])
                seq.append(p[1]['seq'])
                host.append(p[1]['host'])
                date.append(p[1]['date'])

    #print(len(acc_num), len(products), len(seq))
    if len(acc_num) == len(products) == len(seq):
        term = "There were %d sequences found for %s!" % (len(acc_num), virus)
        print(term)
    counted_prods = list(Counter(products))
    counted_source = Counter(source)

    zipped = list(zip(acc_num, products, country, seq, host, date))


    for count in counted_prods:
        # t = count.replace(' ', '_')
        # t_t = t.replace(',', '__')
        # name = t_t.replace('/','__')

        name = name_fixer(count)
        file_guts = "data/%s/%s_%s.fasta" % (virus, virus, name)
        #print("this is the file name: ", file_name)
        with open(file_guts, 'w') as out:
            for line in zipped:
                if count == line[1]:
                    acc_num = line[0]
                    place = line[2].replace(' ', '-')
                    seq = line[3]
                    host = line[4].replace(' ', '-')
                    date = line[5].replace(' ', '-')
                    header = acc_num + "_" + place + "_" + date + "_" + host
                    out.write(">{}\n{}\n".format(header, seq))


