#import pdb; pdb.set_trace()
import pandas as pd

## import all functions from python ##
from python.parser import xml_data_grabber
from python.json_to_json import virus_json
from python.json_to_fasta import fasta_maker
from python.fasta_to_country import country_fasta
from python.region_fasta import region_fasta

## getting all viruses, and countries associated with GLRaV3 and the CP
df_v, df_c = pd.read_csv("data/csv/all_viruses.csv"),  pd.read_csv("data/csv/GLRaV3_countries.csv")
viruses, countries = df_v["virus"].to_list(), df_c["country"].to_list() 
regions = ["USA-all", "CHINA-all", "SPAIN-all"]

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
      out_fs = expand("data/fasta/{country}_Grapevine_leafroll_associated_virus_3.fasta", country=countries)
    run:
      country_fasta(input.in_fs, output.out_fs, countries)

#####################################################################
# This rule will read in the master fasta file from the json_to_fasta
# and it will CAT the fastas into 3 regions: USA, CHINA, SPAIN 
####################################################################
rule regions_fasta:
    input:
      in_f = rules.json_to_fasta.output.out_f
    output:
      out_fs = expand("data/fasta/{region}_Grapevine_leafroll_associated_virus_3.fasta", region=regions)
    run:
      region_fasta(input.in_f, output.out_fs, regions)

###################################################################
# This rule will read in the fasta file from the previous rule
# and run it through the HYPHYMP pre-msa.bf which outputs a
# codon aware, translated protein sequence
####################################################################
rule hyphy_pre:
    input:
      in_fs = rules.regions_fasta.output.out_fs 
    output:
      out_nucs = expand("data/fasta/{region}_Grapevine_leafroll_associated_virus_3.fasta_nuc.fas", region=regions),
      out_prots = expand("data/fasta/{region}_Grapevine_leafroll_associated_virus_3.fasta_protein.fas", region=regions)
    
    shell:
      "for i in {input}; do ~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res hyphy-analyses/codon-msa/pre-msa.bf --input $i; done;"

####################################################################
# This rule will read in the fasta file from the previous rule
# and align the nucleotide file with MAFFT
####################################################################
rule aligner:
    input:
      in_fs = rules.hyphy_pre.output.out_prots
    output:
      out_prots = expand("data/fasta/{region}_Grapevine_leafroll_associated_virus_3_aligned.fasta_protein.fas", region=regions)
    shell:
      "mafft {input.in_fs[0]} > {output.out_prots[0]} 2> mafft_err.txt && mafft {input.in_fs[1]} > {output.out_prots[1]} 2> mafft_err.txt && mafft {input.in_fs[2]} > {output.out_prots[2]} 2> mafft_err.txt"       

####################################################################
# This rule will read in the aligned nuc fasta file from the previous 
# rule ALONG WITH the protein fasta and run it through the 
# HYPHYMP post-msa.bf where we DO NOT compress duplicate sequences  
####################################################################
rule hyphy_post:
    input:
      in_nucs = rules.hyphy_pre.output.out_nucs,
      in_prots = rules.aligner.output.out_prots
    output:
      out_msa = expand("data/fasta/{region}_Grapevine_leafroll_associated_virus_3_aligned.msa", region=regions)
    shell:
      "~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res hyphy-analyses/codon-msa/post-msa.bf --protein-msa {input.in_prots[0]} --nucleotide-sequences {input.in_nucs[0]} --output {output.out_msa[0]} --compress No && ~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res hyphy-analyses/codon-msa/post-msa.bf --protein-msa {input.in_prots[1]} --nucleotide-sequences {input.in_nucs[1]} --output {output.out_msa[1]} --compress No && ~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res hyphy-analyses/codon-msa/post-msa.bf --protein-msa {input.in_prots[2]} --nucleotide-sequences {input.in_nucs[2]} --output {output.out_msa[2]} --compress No"

####################################################################
# This rule will read in the msa files from the previous rule and 
# run it through the HYPHYMP FUBAR analysis 
####################################################################


####################################################################
# This rule will read in the results of FUBAR and the end ...
####################################################################






