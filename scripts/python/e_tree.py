import xml.etree.ElementTree as et
from collections import Counter
import json

#gpgv_file = 'GPGV_sequence.gbc.xml'
#gva_file = 'GVA_sequence.gbc.xml'
front = '../../data/'
glrav3_file = front + 'GLRaV3/NCBI_data/GLRaV3_sequence.gbc.xml'
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

def get_info(elem):
    acc_num = []
    source = []
    seq = []

    acc_num.append(elem.find("INSDSeq_accession-version").text)
    source.append(elem.find("INSDSeq_source").text)
    seq.append(elem.find("INSDSeq_sequence").text)

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
    

    country = checker(get_kids('country'))
    product = checker(get_kids('product'))
    pro_id = checker(get_kids('protein_id'))
    trans = checker(get_kids('translation'))
    host = checker(get_kids('host'))
    date = checker(get_kids('collection_date'))

    #print(acc_num, source, seq, country, product, pro_id, trans, host, date, '\n')
    
    total_info = list(zip(acc_num, source, seq, country, product, pro_id, trans, host, date))
    return total_info
    


root = tree.getroot()
all_info = list(map(get_info, root.findall("INSDSeq")))


my_dict = {}
for info in all_info:
    temp = {}
    for i in info:
        temp = {}
        temp[i[0]] = {'source': i[1], 'seq': i[2], 'country': i[3], 'product': i[4], 'host': i[7], 'date': i[8]}
        my_dict.update(temp)
#print(my_dict)


data = json.dumps(my_dict)
#print(data)

prefix = '../../data/'
data_file = prefix + 'GLRaV3/NCBI_data/GLRaV3_sequence.json'
with open(data_file, 'w') as out_file:
    out_file.write(data)



