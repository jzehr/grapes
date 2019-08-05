import xml.etree.ElementTree as et
import json

#gpgv_file = 'GPGV_sequence.gbc.xml'
#gva_file = 'GVA_sequence.gbc.xml'

# front = '../../data/'
# glrav3_file = '../data/GLRaV3/NCBI_data/GLRaV3_sequence.gbc.xml'

def xml_reader(in_file, out_file):
    virus_in_file = in_file
    virus_out_file = out_file
    tree = et.parse(virus_in_file)

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
            # elif len(temp) == 1:
            #     temp = str(temp[0])
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

        # print(len(product), len(trans))
        # print('\n')
        acc_str = str(acc_num[0])

        my_dict = {}
        my_dict[acc_str] = {'source': source, 'seq': seq, 'country': country, 'product': product, 'pro_id': pro_id, 'trans': trans, 'host': host, 'date': date}
        #print(type(product))

       
        #print(acc_num, source, seq, country, product, pro_id, trans, host, date, '\n')
        #print(len(product), len(acc_num), len(source), len(pro_id), len(trans))
        #print('\n')
        #total_info = list(zip(acc_num, source, seq, country, product, pro_id, trans, host, date))

        # print(type(my_dict))
        # print(my_dict)
        # print('\n')
        return my_dict
        


    root = tree.getroot()
    temp_info = list(map(get_info, root.findall("INSDSeq")))

    '''
    not sure why i have to do this but it is a little annoying
    '''

    all_info = {}
    for i in temp_info:
        all_info.update(i)
    
    data = json.dumps(all_info)
    with open(virus_out_file, 'w') as out_file:
        out_file.write(data)



