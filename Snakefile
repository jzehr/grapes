#import pdb; pdb.set_trace()

## import all functions from ~ my ~ python dir ##
from python.helper import name_fixer
from python.flat import flatten
from python.nexus_parser import nexus
## might need to set node limits to run on ## 
# only runs on node 5 right now 


# setting HYPHYMP var #
#HYPHY = "/home/jordanz/grapes/hyphy-develop/hyphy LIBPATH=/home/jordanz/hyphy/res"
HYPHY = "~/grapes/hyphy-develop/hyphy LIBPATH=/home/jordanz/grapes/hyphy-develop/res"
PRE = "~/grapes/hyphy-analyses/codon-msa/pre-msa.bf"
POST = "~/grapes/hyphy-analyses/codon-msa/post-msa.bf"
GARD = "~/grapes/hyphy-develop/res/TemplateBatchFiles/GARD.bf"
MEME = "~/grapes/hyphy-develop/res/TemplateBatchFiles/SelectionAnalyses/MEME.bf"
FEL_contrast = "~/grapes/hyphy-develop/res/TemplateBatchFiles/SelectionAnalyses/FEL-contrast.bf"

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
   "{HYPHY} {PRE} --input {input.in_f}"
 
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
   "{HYPHY} {POST} --protein-msa {input.in_prot} --nucleotide-sequences {input.in_nuc} --output {output.out_f} --compress No"
 
####################################################################
# This rule will read in the post-hyphy fasta 
# and run it through ~ GARD ~
####################################################################
rule rpf_GARD:
  input:
    in_f = rules.rpf_post.output.out_f
  output:
    out_j = str(rules.rpf_post.output.out_f) + ".GARD.json",
    out_nex = str(rules.rpf_post.output.out_f) + ".best-gard"
  shell:
   "{HYPHY} {GARD} --alignment {input.in_f}"

######################################################################
# This rule will read in the output from GARD 
# and run it through a NEXUS parser to send each partition
# to a fasta file
#####################################################################
rule rpf_nexus:
  input:
    in_f = rules.rpf_GARD.output.out_nex
  output:
    out_f = dynamic("data/fasta/{RPF}.hyphy.fas.GARD.{n}.nex")
  run:
    nexus(input.in_f, output.out_f)

####################################################################
# This rule will read in the output from the NEXUS parser  
# and run it through ~ MEME ~
#####################################################################
rule rpf_MEME:
  input:
    in_f = rules.rpf_nexus.output.out_f
  output:
    out_j = dynamic("data/fasta/{RPF}.hyphy.fas.GARD.{n}.nex.MEME.json")
  shell:
   "{HYPHY} {MEME} --alignment {input.in_f}"
 
######################################################################
# This rule will read in the output from MEME 
# and run it through ~ FEL-contrast ~
###################################################################
#rule rpf_Fc:
#  input:
#    in_f = rules.rpf_GARD.output.out_prot
#  output:
#    out_j = dynamic("data/fasta/{RPF}.hyphy.fas.GARD.{n}.nex.FEL.json")
#  shell:
#   "{HYPHY} {FEL_contrast} --input {input.in_f}"

######################################################################
# This rule will read in the output from GARD, MEME, and FEL-contrast 
# and send it out to be visualized 
###################################################################
#rule rpf_Fc:
#  input:
#    in_GARD = rules.rpf_GARD.output.out_j,
#    in_MEME = rules.rpf_MEME.output.out_j,
#    in_FELc = rules.rpf_Fc.output.out_j
#  output:
#    out_nuc = "data/fasta/{RPF}.fasta_nuc.fas"
#  shell:
#   "{HYPHY} {FEL_contrast} --input {input.in_f}"




