#import pdb; pdb.set_trace()

## import all functions from python ##
from python.helper import name_fixer
from python.seq_blaster import blaster


with open("rsrc/GLRaV3_regions.json") as regions_json:
  data_dict = json.load(regions_json)

REGIONS = list(data_dict.keys())


## expand(products=data[REGIONS][1])

####################################################################
# This rule will read in the XML file from NCBI and parse it
# into a master JSON
####################################################################
rule region_fasta_to_orfs:
  input:
    in_f = "data/fasta/{REGION}_all.fasta"
  output:
    out_f = "data/fasta/{REGION}_orf_{ORF}.fasta"
  run:
   blaster(input.in_f, output.out_f)
   #import pdb;pdb.set_trace()
 
