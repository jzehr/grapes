#import pdb; pdb.set_trace()

## import all functions from ~ my ~ python dir ##
from python.helper import name_fixer
from python.flat import flatten

# setting HYPHYMP var #
HYPHYMP = "~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res"

# making a list of all the poteins from each region
# that had more then 1 sequence
with open("data/GOOD_PRODS.json") as gps:
  data = json.load(gps)

temp_files = []
for key, item in data.items():
  f = [key + "_" + i for i in item]
  temp_files.append(f)

reg_prod_files = flatten(temp_files)
# example ~ EUROPE_hsp70_like ~ # 

## need to add a rule ALL ##

####################################################################
# This rule will read in a reg_prod_file and run it through pre-bf
####################################################################
rule rpf_pre:
  input:
    in_f = "data/fasta/{RPF}.fasta"
  output:
    out_prot = "data/fasta/{RPF}.fasta_protein.fas",
    out_nuc = "data/fasta/{RPF}.fasta_nuc.fas"
  shell:
   "{HYPHYMP} /home/jordanz/grapes/hyphy-analyses/codon-msa/pre-msa.bf --input {input.in_f}"
 
####################################################################
# This rule will read protein fas from previous rule and
# align it with MAFFT
####################################################################
rule mafft_rpf:
  input:
    in_prot = rules.rpf_pre.output.out_prot
  output:
    out_prot = "data/fasta/{RPF}.fasta_protein_aligned.fas"
  shell:
    "mafft --quiet {input.in_f} > {output.out_prot}"

####################################################################
# This rule will read in aligned PROTEIN file  
# and run it through post-bf
####################################################################
rule rpf_post:
  input:
    in_prot = rules.mafft_rpf.output.out_prot,
    in_nuc = rules.rpf_pre.output.out_nuc
  output:
    out_f = "data/fasta/{RPF}.hyphy.fas"
  shell:
   "{HYPHYMP} /home/jordanz/grapes/hyphy-analyses/codon-msa/post-msa.bf --protein-msa {input.in_prot} --nucleotide-sequences {input.in_nuc} --output {output.out_f} --compress No"
 
####################################################################
# This rule will read in the post-hyphy fasta 
# and run it through ~ GARD ~
####################################################################
rule rpf_GARD:
  input:
    in_f = rules.rpf_post.output.out_f
  output:
    out_prot = str(rules.rpf_post.output.out_f) + ".GARD.json"
  shell:
   "{HYPHYMP} GARD --alignment {input.in_f} --type Nucleotide --code Universal"

#####################################################################
# This rule will read in the output from GARD 
# and run it through ~ MEME ~
#####################################################################
#rule rpf_MEME:
#  input:
#    in_f = "data/fasta/{RPF}.fasta"
#  output:
#    out_prot = "data/fasta/{RPF}.fasta_protein.fas",
#    out_nuc = "data/fasta/{RPF}.fasta_nuc.fas"
#  shell:
#   "{HYPHYMP} /home/jordanz/grapes/hyphy-analyses/codon-msa/pre-msa.bf --input {input.in_f}"
 
######################################################################
# This rule will read in the output from MEME 
# and run it through ~ FEL-contrast ~
###################################################################
#rule rpf_Fc:
#  input:
#    in_f = "data/fasta/{RPF}.fasta"
#  output:
#    out_prot = "data/fasta/{RPF}.fasta_protein.fas",
#    out_nuc = "data/fasta/{RPF}.fasta_nuc.fas"
#  shell:
#   "{HYPHYMP} /home/jordanz/grapes/hyphy-analyses/codon-msa/pre-msa.bf --input {input.in_f}"
 
