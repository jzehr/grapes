#import pdb; pdb.set_trace()
import pandas as pd

## import all functions from python ##
from python.parser import xml_data_grabber
from python.json_to_json import virus_json
from python.json_to_fasta import fasta_maker
from python.fasta_to_country import country_fasta
from python.region_fasta import region_fasta

regions = [
            "EUROPE", 
            "SOUTH_AMERICA", 
            "NORTH_AMERICA", 
            "MIDDLE_EAST", 
            "NORTH_AFRICA", 
            "SOUTH_AFRICA", 
            "ASIA", 
            "OCEANIA"
          ]


rule targets:
  input:
    expand("data/{region}_this.txt", region=regions)

rule a:
  input:
    "rsrc/GLRaV3_10-2-19_sequence.gbc.xml"
  output:
    expand("data/{region}.txt", region=regions)
  shell:
    "touch {output}"

rule b:
  input:
    "data/{regions}.txt"
  output:
    "data/{regions}_this.txt"
  shell:
    "touch {output}"

