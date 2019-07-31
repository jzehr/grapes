### turn this into large class file, could be fun ###

import json

import xml.etree.ElementTree as et
from collections import Counter
import json


viruses = ['GLRaV3', 'GVA', 'GPGV']
#viruses = ['GLRaV3']

def get_info(elem):

    virus_source = elem.find("INSDSeq_source").text

    def checker(lst):
        temp = lst
        if len(temp) == 0:
            temp.append('no_value')
        return temp
    
    def get_kids(word):
        temp = list(elem.iter('INSDQualifier'))
        temp_word = filter(lambda x: x.find('INSDQualifier_name').text == word, temp)
        new_word = list(map(lambda x: x.find('INSDQualifier_value').text, temp_word))
        return new_word
    
    product = checker(get_kids('product'))

    return virus_source, product


def filt_info(tup):
    source = tup[0]
    prod = tup[1]
    
    '''
    this part is fragile... need to fix 
    '''
    master = ['Grapevine virus A',\
     'Grapevine virus A (GVA)',\
     'Grapevine leafroll-associated virus 3 (GLRaV-3)',\
     'Grapevine leafroll-associated virus 3m',\
     'Grapevine Pinot gris virus','Grapevine Pinot gris virus']

    if source in master:
        return prod

def name_fixer(count):
        temp = count.replace(' ', '_')
        t_t = temp.replace(',', '__')
        name = t_t.replace('/','__')
        return name

def f_name(virus, counted_item):
    f_n = "data/%s/%s_%s.fasta" % (virus, virus, counted_item)
    #print(f_name)
    return f_n


for virus in viruses:
    v_file = '%s/NCBI_data/%s_sequence.gbc.xml' % (virus, virus)
    
    tree = et.parse(v_file)
    root = tree.getroot()

    all_info = list(map(get_info, root.findall("INSDSeq")))
    temp_info = list(map(filt_info, all_info))
    temp_filt = list(filter(lambda x: x != None, temp_info))
    #print(virus, len(temp_info), len(temp_filt))

    new_filt = [i for l in temp_filt for i in l]
    counted_filt = list(Counter(new_filt).keys())
    
    corrected = list(map(name_fixer, counted_filt))
    
    f_names = [(pos +1, f_name(virus, i)) for pos, i in enumerate(corrected)]
    
    
    my_dict = {}
    my_dict[virus] = {}
    for item in f_names:
        num = item[0]
        name = item[1]
        my_dict[virus][num] = name
        my_dict.update(my_dict)

    #print(my_dict)

    data = json.dumps(my_dict)
    json_file = '%s_config.json' % virus
    
    print('Writing: %s config \n' % virus)
    
    with open(json_file, 'w') as out_file:
        out_file.write(data)

    # print('\n')


