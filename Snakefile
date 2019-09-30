#import pdb; pdb.set_trace()
import pandas as pd

## import all functions from python ##
from python.parser import xml_data_grabber
from python.json_to_json import virus_json
from python.json_to_fasta import fasta_maker
from python.fasta_to_country import country_fasta

## getting all viruses, and countries associated with GLRaV3 and the CP
df_v, df_c = pd.read_csv("data/csv/all_viruses.csv"),  pd.read_csv("data/csv/GLRaV3_countries.csv")
viruses, countries = df_v["virus"].to_list(), df_c["country"].to_list() 
regions = ["USA", "CHINA", "SPAIN"]

#importants = ["leafroll_associated_virus_3","virus_A","Pinot_gris_virus"]
importants = ["leafroll_associated_virus_3"]

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
      in_f = "rsrc/09-16-2019_grapevine.gbc.xml",
    output:
      out_full = "data/json/09-16-2019_grapevine.json"
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
     out_f = expand("data/json/{virus}.json", virus=viruses) 
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
rule json_to_fasta:
  input:
    in_f = "data/json/Grapevine_leafroll_associated_virus_3.json"
  output:
    out_f = "data/fasta/Grapevine_leafroll_associated_virus_3.fasta", 
    out_csv = "data/csv/Grapevine_leafroll_associated_virus_3.csv"
  run:
    fasta_maker(input.in_f, output.out_f, output.out_csv)
    
####################################################################
# This rule will read in the fasta file from the previous rule and 
# separate out sequences based on location of where they were collected
####################################################################
rule country_fasta:
  input:
    in_fs = rules.json_to_fasta.input.in_f
  output:
    out_fs = expand("data/fasta/{country}_Grapevine_{important}.fasta", country=countries, important=importants)
  run:
    country_fasta(input.in_fs, output.out_fs, countries)

#####################################################################
# This rule will read in the master fasta file from the json_to_fasta
# and it will CAT the fastas into 3 regions: USA, CHINA, SPAIN 
####################################################################
#rule regions_fasta:
#  input:
#    in_f = rules.json_to_fasta.output.out_f
#  output:
#    out_fs = expand("data/fasta/{region}_Grapevine_{important}.fasta", region=regions, important=importants)
#  run:
#    import pdb;pdb.set_trace()



###################################################################
# This rule will read in the fasta file from the previous rule
# and run it through the HYPHYMP pre-msa.bf which outputs a
# codon aware, translated protein sequence
####################################################################


####################################################################
# This rule will read in the fasta file from the previous rule
# and align the nucleotide file with MAFFT
####################################################################


####################################################################
# This rule will read in the aligned nuc fasta file from the previous 
# rule ALONG WITH the protein fasta and run it through the 
# HYPHYMP post-msa.bf 
####################################################################


####################################################################
# !! This rule will read in the aligned nuc fasta file from the previous 
# rule ALONG WITH the protein fasta and run it through the 
# HYPHYMP post-msa.bf 
####################################################################


####################################################################
# !! This rule will read in the aligned nuc fasta file from the previous 
# rule ALONG WITH the protein fasta and run it through the 
# HYPHYMP post-msa.bf 
####################################################################






