#import pdb; pdb.set_trace()

## import all functions from python ##
from python.helper import name_fixer
from python.flat import flatten
#from python.seq_blaster import blaster

with open("data/GOOD_PRODS.json") as gps:
  data = json.load(gps)

temp_files = []
for key, item in data.items():
  f = [key + "_" + i for i in item]
  temp_files.append(f)

region_prods = flatten(temp_files)
print(files)

## expand(products=data[REGIONS][1])

####################################################################
# This rule will read in the each REGION fasta file and 
# split it into the ORFS from that region
#
# can use an input function to see how many ORFs will be made for each?
####################################################################
rule region_fasta_to_orfs:
  input:
    in_f = "data/fasta/{REGION}_all.fasta"
  output:
    out_f = "data/fasta/{REGION}_orf.fasta"
  run:
   #blaster(input.in_f, output.out_f)
   import pdb;pdb.set_trace()
 
