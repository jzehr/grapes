### turn this into large class file, could be fun ###
import os

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
    new = []
    bad = [' ',',','.','/','-','(',')',':']
    for char in list(count):
        if not char in bad:
            new.append(char)
        else:
            new.append('_')
    temp = ''.join(new)
    name = temp.replace('__','_')

    return name

'''
this is the meat and potatoes of the script
'''
for virus in viruses:

    v_file = 'NCBI/%s_sequence.gbc.xml' % virus

    tree = et.parse(v_file)
    root = tree.getroot()

    all_info = list(map(get_info, root.findall("INSDSeq")))
    temp_info = list(map(filt_info, all_info))
    temp_filt = list(filter(lambda x: x != None, temp_info))

    new_filt = [i for l in temp_filt for i in l]
    counted_filt = list(Counter(new_filt).keys())

    corrected = list(map(name_fixer, counted_filt))
    #corrected = corrected_temp[0]

    my_dict = {}
    my_dict = {virus: corrected}

    #print(my_dict)
    data = json.dumps(my_dict)
    json_file = '../data/%s_config.json' % virus

    print('Adding: %s to a config file \n' % virus)

    with open(json_file, 'w') as out_file:
        out_file.write(data)



