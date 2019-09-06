import os
import json
import xml.etree.ElementTree as et
from collections import Counter
import ast


'''
    ** The data structure used will be a dictionary **

            STEPS IN SCRIPT
            ---------------
    1. rip all desired data from the XML file and store it as a dict
    2. add the data to a dictionary,
    3. append the dictionary to a json file

 '''

def xml_data_grabber(input_file, output_file):
    '''
    This will rip date from the XML and
    write it to a JSON file
    '''
    input_f = str(input_file)
    output_f = str(output_file)

    ## in --> str | out --> str ##
    def name_fixer(string):
        new = []
        bad_chars = [' ',',','.','/','-','(',')',':']

        def checker(char):
            if char in bad_chars:
                return '_'
            else:
                return char

        for char in list(string):
            new.append(checker(char))

        temp = ''.join(new)
        name = temp.replace('__','_')
        return name

    ## in --> INSDSeq element | out --> dict ##
    def rip_info(elem):

        data = {}

        viral_source = name_fixer(str(elem.find("INSDSeq_definition").text))
        accession_number = name_fixer(str(elem.find("INSDSeq_accession-version").text))
        create_date =  name_fixer(str(elem.find("INSDSeq_create-date").text))

        acc_date = (accession_number, create_date)

        data[viral_source] = acc_date

        ## in --> list | out --> list ##
        def checker(lst):
            temp = lst
            if len(temp) == 0:
                temp.append("no_value")
            return temp

        ## in --> INSDQualifier_name | out --> (list of values) INSDQualifier_value ##
        def get_qualifier(word):
            temp = list(elem.iter("INSDQualifier"))
            temp_word = filter(lambda x: x.find("INSDQualifier_name").text == word, temp)
            new_word = list(map(lambda x: x.find("INSDQualifier_value").text, temp_word))
            return new_word

        ## in --> INSDFeature_key | out --> INSDFeature_location ##
        def get_feature(word):
            temp = list(elem.iter("INSDFeature"))
            temp_word = filter(lambda x: x.find("INSDFeature_key").text == word, temp)
            new_word = list(map(lambda x: x.find("INSDFeature_location").text, temp_word))
            return new_word

        quals = ["organism","product", "note", "strain", "isolate", "country", "host", "collection_date", "translation"]
        features = ["CDS"]

        for q in quals:
            data[q] = checker(get_qualifier(q))

        for f in features:
            data[f] = checker(get_feature(f))

        data["nuc_seq"] = str(elem.find("INSDSeq_sequence").text)

        return  data

    tree = et.parse(input_f)
    root = tree.getroot()
    temp_info = list(map(rip_info, root.findall("INSDSeq")))

    info = [str(i) for i in temp_info]

    json_file = output_f


    if os.path.exists(json_file):
        cmd = "rm -f " + json_file
        os.system(cmd)

    for i in info:
        parsed_data = ast.literal_eval(i)
        with open(json_file,"a") as f:
            json.dump(parsed_data, f, indent=3)

