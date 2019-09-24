#import pdb; pdb.set_trace()
import pandas as pd

## import all functions from python ##
from python.parser import xml_data_grabber
from python.json_to_json import virus_json
from python.json_to_fasta import fasta_maker
from python.fasta_to_country import country

## getting all viruses, and countries associated with GLRaV3 and the CP
df_v, df_c = pd.read_csv("data/all_viruses.csv"),  pd.read_csv("data/GLRaV3_countries.csv")
viruses, countries = df_v["virus"].to_list(), df_c["country"].to_list(), 

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
      out_full = "data/09-16-2019_grapevine.json"
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
    in_f = expand("data/json/Grapevine_{important}.json", important=importants)
  output:
    out_f = expand("data/fasta/Grapevine_{important}.fasta", important=importants), 
    out_csv = expand("data/csv/Grapevine_{important}.csv", important=importants)
  run:
    zipped = list(zip(input.in_f, output.out_f, output.out_csv))
    for z in zipped:
      	in_file = z[0]
      	out_fasta = z[1]
        out_csv = z[2]

      	fasta_maker(in_file, out_fasta, out_csv)


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
    country(input.in_fs, output.out_fs, countries)

####################################################################
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






