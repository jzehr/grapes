#import pdb; pdb.set_trace()

## import all functions from python ##
from python.parser import xml_data_grabber
from python.json_to_json import virus_json


viruses = []
with open("data/input/all_viruses.txt") as in_f:
  data = in_f.readlines()
  for line in data:
    viruses.append(line.strip())

####################################################################
# This is the rule "all" which will run all the rules to produce
# the tree files as outputs
####################################################################
#rule all: 
#  input:
#    "data/total_viral_sequences_09-05-19.json"
    #"data/temp.json", 
    

####################################################################
# This rule will read in the XML file from NCBI and parse it 
# into a master JSON
####################################################################
rule xml_to_json:
    input:
      #in_f = "data/input/temp_new.xml"
      in_f = "data/input/total_viral_sequences_09-05-19.gbc.xml"
    output:
      out_full = "data/total_viral_sequences_09-05-19.json"
      #out_full = "data/temp.json",
      ## need to add a file that will output all the virus names!!
      
    run:
      xml_data_grabber(input.in_f, output.out_full)

####################################################################
# This rule will read in the JSON file from the previous rule
# and output JSON files with each unique virus present
####################################################################
rule json_to_json:
    input:
      in_f = rules.xml_to_json.output.out_full
    output:
     out_f = expand("data/{virus}.json", virus=viruses) 
     #out_f = "data/total_viral_sequences_09-05-19.json"
    run:
      zipped = list(zip(viruses, output.out_f)) 
      for z in zipped:
        virus = z[0]
        out_file = z[1]
        virus_json(input.in_f, virus, out_file)

####################################################################
# This rule will read in the JSON file from the previous rule
# and output fasta files with ORFs from the Viruses present
#       
#                       ~~ WARNING ~~
# The ORFs might not be in-frame yet, and need to be run through
# a codon cleaner AND ORF cleaner which will trim START and STOP
# codons
####################################################################


