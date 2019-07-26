import xml.etree.ElementTree as et
from collections import Counter
import json

#gpgv_file = 'GPGV_sequence.gbc.xml'
#gva_file = 'GVA_sequence.gbc.xml'
glrav3_file = 'GLRaV3_sequence.gbc.xml'
tree = et.parse(glrav3_file)

'''
root is INSDSet
child is INSDSeq
children is "INSDSeq_blah"
kids are: INSDSeqid, INSDKeyword, INSDReference, INSDFeature 
friends are: INSDFeature_key, INSDReference_reference, INSDReference_position, INSDReference_authors, etc 
cousins are: INSDAuthor, INSDInterval 
cats are: INSDInterval_from, INSDInterval_to, INSDInterval_accession, INSDQualifier_name, INSDQualifier_value 
'''

def get_sequence_children(elem):
    def checker(lst):
        lst = lst
        if len(lst) == 0:
            lst.append('no_value')
        return lst


    acc_num = []
    source = []
    seq = []

    acc_num.append(elem.find("INSDSeq_accession-version").text)
    source.append(elem.find("INSDSeq_source").text)
    seq.append(elem.find("INSDSeq_sequence").text)

    temp_country = list(elem.iter('INSDQualifier'))
    f_temp_country = filter(lambda x: x.find('INSDQualifier_name').text == 'country', temp_country)
    m_temp_country = list(map(lambda x: x.find('INSDQualifier_value').text, f_temp_country))
    country = checker(m_temp_country)

    temp_products = list(elem.iter('INSDQualifier'))
    f_temp_products = filter(lambda x: x.find('INSDQualifier_name').text == 'product', temp_products)
    m_temp_products = list(map(lambda x: x.find('INSDQualifier_value').text, f_temp_products))
    product = checker(m_temp_products)

    temp_pro_id = list(elem.iter('INSDQualifier'))
    f_temp_pro_id = filter(lambda x: x.find('INSDQualifier_name').text == 'protein_id', temp_pro_id)
    m_temp_pro_id = list(map(lambda x: x.find('INSDQualifier_value').text, f_temp_pro_id))
    pro_id = checker(m_temp_pro_id)

    temp_trans = list(elem.iter('INSDQualifier'))
    f_temp_trans = filter(lambda x: x.find('INSDQualifier_name').text == 'translation', temp_trans)
    m_temp_trans = list(map(lambda x: x.find('INSDQualifier_value').text, f_temp_trans))
    trans = checker(m_temp_trans)

    #print(len(acc_num), len(source), len(seq), len(country), len(product), len(pro_id), len(trans))
    #print(acc_num, source, seq, m_temp_country, m_temp_products)
    total_info = list(zip(acc_num, source, country, product, pro_id, trans, seq))
    return total_info
    


root = tree.getroot()
all_info = list(map(get_sequence_children, root.findall("INSDSeq")))
#print(all_info)

my_dict = {}
for i in all_info:
    temp = {}
    for l in i:
        temp = {}
        temp[l[0]] = {'source': l[1], 'country': l[2], 'products': l[3], 'protein_id': l[4], 'translation_of_protein': l[5], 'seq': l[6]}
        my_dict.update(temp)
#print(my_dict)


data = json.dumps(my_dict)
#print(data)

data_file = 'GLRaV3_sequence.json'
with open(data_file, 'w') as out_file:
    out_file.write(data)





