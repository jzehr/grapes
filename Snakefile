
#import pdb; pdb.set_trace()


## import all functions from python ##
from python.parser import xml_data_grabber


####################################################################
# This is the rule "all" which will run all the rules to produce
# the tree files as outputs
####################################################################
rule all: 
  input:
    "data/total_info_09-05-19.json"

####################################################################
# This rule will read in the XML file from NCBI and parse it 
# into a master JSON
####################################################################
rule xml_to_json:
    input:
      in_f = "data/input/total_viral_sequences_09-05-19.gbc.xml"
    output:
      out_f = "data/total_info_09-05-19.json"
    run:
      xml_data_grabber(input.in_f, output.out_f)

