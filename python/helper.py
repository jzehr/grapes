import re
import xml.etree.ElementTree as et
from collections import Counter
import math

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

## in --> INSDSeq element | out --> dict ##
def element_item(elem):

    master = {}
    data = {}

    error = {}

    viral_source = name_fixer(str(elem.find("INSDSeq_definition").text))
    accession_number = name_fixer(str(elem.find("INSDSeq_accession-version").text))
    create_date =  name_fixer(str(elem.find("INSDSeq_create-date").text))

    t = elem.find("INSDSeq_references")
    this = list(t.iter("INSDReference"))
    title = list(map(lambda x: x.find("INSDReference_title").text, this))[0]

    master[accession_number] = data
    data["viral_source"] = viral_source
    data["create_date"] = create_date
    data["title"] = title

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

    def get_ref_doi(word):
        temp = list(elem.iter("INSDXref"))
        temp_word = filter(lambda x: x.find("INSDXref_dbname").text == word, temp)
        new_word = list(map(lambda x: x.find("INSDXref_id").text, temp_word))

        return new_word


    quals = ["organism","product", "note", "strain","isolate", "isolation_source", "country", "host", "collection_date", "translation"]
    features = ["CDS"]
    ref = ["doi"]

    for r in ref:
        data[r] = get_ref_doi(r)

    for q in quals:
        data[q] = checker(get_qualifier(q))

    for f in features:
        data[f] = checker(get_feature(f))

    data["nuc_seq"] = str(elem.find("INSDSeq_sequence").text)

    if len(data["product"]) != len(data["CDS"]):
        error[("prodCDS_length", accession_number)] = data
        return error

    if data["CDS"][0] == data["product"][0]:
        error[("prodCDS_name", accession_number)] = data
        return error

    return master

def write_fasta(data, p, pos, item):
    acc_num = p
    CDS = data[p]["CDS"][pos]
    nuc_seq = data[p]["nuc_seq"]
    orf1_s = int(re.findall(r'\d+', CDS.split("..")[0])[0]) - 1
    orf1_e = int(re.findall(r'\d+', CDS.split("..")[1])[0])
    if data[p]["collection_date"][0] == "no_value":
        date = data[p]["create_date"]
    else:
        date = data[p]["collection_date"][0]
    country = data[p]["country"][0]
    host = data[p]["host"][0]
    strain = data[p]["strain"][0]
    isolate = data[p]["isolate"][0]
    iso_source = data[p]["isolation_source"][0]
    nuc_seq = data[p]["nuc_seq"]
    seq = nuc_seq[orf1_s:orf1_e]

    header = "%s_%s_%d_%s_%s_%s_%s_%s_%s" % (name_fixer(acc_num), name_fixer(item), pos, name_fixer(date), name_fixer(country), name_fixer(host), name_fixer(strain), name_fixer(isolate), name_fixer(iso_source))
    header = header.replace("__","_")
    row = (name_fixer(acc_num), name_fixer(item), pos, name_fixer(date), name_fixer(country), name_fixer(host), name_fixer(strain), name_fixer(isolate))
    return header, seq, row

def distance(location_1, location_2):
    lat1, lon1 = location_1
    lat2, lon2 = location_2
    radius = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
	    math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d





