#!/bin/bash


echo " ~gathering all your information ~"

# this will read in your XML from NCBI
# it spits out a json of locations separated by regions
python python/all_country_json.py --file rsrc/GLRaV3_10-2-19_sequence.gbc.xml

# this script will read in that XML file and split it into 
# JSONs of products that have more than 2 sequences
# and fasta files for each region and product
python python/region_seq.py -x rsrc/GLRaV3_10-2-19_sequence.gbc.xml -j rsrc/GLRaV3_regions.json



