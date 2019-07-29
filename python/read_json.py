import json
from collections import Counter 

'''
1. should separate based on:
    "protein type"

2. then append country to the sequence header + the accession number

'''




#file = 'GVA/GVA_sequence.json'
front = '../../data/'
file = front + 'GLRaV3/NCBI_data/GLRaV3_sequence.json'
#file = 'GPGV/GPGV_sequence.json'

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
        #if p[1]['source'] == 'Grapevine virus A' or p[1]['source'] == 'Grapevine virus A (GVA)':
        if p[1]['source'] == 'Grapevine leafroll-associated virus 3 (GLRaV-3)' or p[1]['source'] == 'Grapevine leafroll-associated virus 3m':
        #if p[1]['source'] == 'Grapevine Pinot gris virus':
            acc_num.append(p[0])
            products.append(p[1]['product'])
            source.append(p[1]['source'])
            country.append(p[1]['country'])
            seq.append(p[1]['seq'])
            host.append(p[1]['host'])
            date.append(p[1]['date'])

#print(len(acc_num), len(products), len(seq))
counted_prods = list(Counter(products))
counted_source = Counter(source)
#print(counted_source)

zipped = list(zip(acc_num, products, country, seq, host, date))

for count in counted_prods:
    #print("before: ", count)
    t = count.replace(' ', '_')
    #print("this is t: ", t)
    t_t = t.replace(',', '__')
    #print("this is t_t: ", t_t)
    name = t_t.replace('/','__')
    #print("this is name: ", name)
    # print('\n')
    file_name = front + 'GLRaV3/GLRaV3_' + name + '.fasta'
    #print("this is the file name: ", file_name)
    with open(file_name, 'w') as out:
        for line in zipped:
            #print('this is from the json: ', line[1])
            if count == line[1]:
                #print(line[2])
                acc_num = line[0]
                place = line[2].replace(' ', '-')
                seq = line[3]
                host = line[4].replace(' ', '-')
                date = line[5].replace(' ', '-')
                #print("this is the place: ", place)
                header = acc_num + "_" + place + "_" + date + "_" + host
                out.write(">{}\n{}\n".format(header, seq))


