
#import pdb; pdb.set_trace()


## import all functions from python ##
#from python.test import just_print
from python.json_part_list import list_maker
from python.flat import flatten
from python.e_tree import xml_reader
from python.read_json import json_to_fasta
# from python.cat_files import catter

## add this so that you can call it from here instead of running it separately ##
# shell("python3 rsrc/config_json.py")

## these are the variables from the grape viruses ##
viruses = ['GLRaV3', 'GPGV', 'GVA']
#viruses = ['GLRaV3']

input_files = ['rsrc/NCBI/%s_sequence.gbc.xml' %  v for v in viruses]

#this will read in the virus config files and scrape all the protein parts
#that come from that virus
#example: heat schock protein 70-like protein

all_virus = []
for v in viruses:
    temp_file = 'data/%s_config.json' % v
    all_virus.append(list_maker(temp_file, v))
all_virus_proteins = flatten(all_virus)


####################################################################
# This is the rule "all" which will run all the rules to produce
# the tree files as outputs
####################################################################
rule all: 
  input:
    'data/tree/GLRaV3_coat_protein_cat_align.fasta.treefile', 'data/tree/GPGV_coat_protein_cat_align.fasta.treefile', 'data/tree/GVA_coat_protein_cat_align.fasta.treefile'

####################################################################
# This rule will read in the XML files from NCBI and parse them into JSONs
####################################################################
rule xml_to_json:
    #params:
        #viruses = viruses
    output:
        expand('data/{virus}.json', virus=viruses)
    run:
        zipped = list(zip(viruses, input_files, output))
        for i in zipped:
            virus = i[0]
            in_file = i[1]
            out_file = i[2]
            print("Virus: ",virus," from GenBank XML file --> ",in_file, "printing to -->", out_file)
            xml_reader(in_file, out_file)
            print('\n')

####################################################################
# This rule will read in the JSON from the previous rule and create Fasta files 
# for EACH protein represented within each virus
####################################################################
rule json_to_fasta:
    #params:
        #all_virus_proteins=all_virus_proteins
    input:
        virus_xml = rules.xml_to_json.output
    output:
        all_outs = expand("data/{temp}.fasta" , temp=all_virus_proteins)
    run:
        json_to_fasta(input.virus_xml, output.all_outs, viruses)

####################################################################
#               *** WARNING ***
# ~ this might be an extremely fragile bit of the code ~
# 
# This rule might be a little annoying, 
# i will need to think of an elegant way to handle this... 
####################################################################
rule cat_files:
    input:
        in_files=rules.json_to_fasta.output.all_outs
    output:
        outs_temp = expand("data/{virus}_coat_protein_temp_cat.fasta" , virus=viruses)
    run:
        for v in viruses:
            print("cat-ing this virus: ", v)
            shell("bash bash/cat_%s.sh" % v)
            print('\n')

####################################################################
#               *** WARNING ***
# ~ this might be an extremely fragile bit of the code ~
#
# This rule will clean sequences out of the cat files 
# some sequences are clearly mislabeled 
####################################################################
rule cat_cleaner:
    input:
        in_files=rules.cat_files.output.outs_temp
    output:
        outs_cat = expand("data/{virus}_coat_protein_cat_cleaned.fasta" , virus=viruses)
    run:
        zipped = list(zip(viruses, input.in_files, output.outs_cat))
        for z in zipped:
            virus = z[0]
            temp_file = z[1]
            out_file = z[2]
            with open(temp_file, "r") as in_put:
                with open(out_file, "w") as out_put: 
                    for pos, line in enumerate(in_put):
                        # print(pos, [line])
                        bad_1 = 'MGAYTHVDFHESRLLKDKQDYLSFKSANEAPPDPPGYVRPDSYVRAYLIQRADFPNTQSLSVTLSVASNKLASGLMGSDAVSSSFMLMNDAGDYFECGVCHNKPYLGREVIFCRKYIGGRGVEITTGKNYTSNNWNETSYVIQVNVVDGLAQTTVNSTYTQTDVSGLPKNWTRIYKITKIVSVDQNLYPGCFSDSKLGVMRIRSLLVSPVRIFFRGILLKPLKKSFNARIEDVLNIDDTSLLEPSPVVPESTGGVGPSEQLDVVALTSDVTELINTRGQGKICFPDSVLSINEADIYDERYLPITEALQINARLRRLVLSKGGSQTPRDMGNMIVAMIQLFVLYSTVKNISVKDGYRVETELGQKKVYLSYSEVREAILGGKYDASPTNTVRSFMRYFTHTTITLLIEKKIQPAYTALAKHGVPKRFTPYCFDFALLDNRYYPADVLKANAMACAIAIKSANLRRKGSETYNILESI\n'
                        bad_2 = '>QCY41301_1_coat_protein_MK804765_1_Brazil_19_Mar_2018_Vitis_sp_cv_BRS_Nubia_hybrid_grapevine_\n'
                        if bad_1 == line or bad_2 == line: 
                            continue 
                        out_put.write(line)

####################################################################
# this rule will read in the cat files and align the contents
####################################################################
rule amino_align:
    input:
        ins = rules.cat_cleaner.output.outs_cat
    output:
        outs = expand("data/{virus}_coat_protein_cat_align.fasta" , virus=viruses)
    run:
        for pos, file in enumerate(input.ins):
            shell("mafft %s > %s" % (file, output.outs[pos]))

####################################################################
# this rule will build all the trees from the aligned files
####################################################################
rule build_trees:
    input:
        in_align = "data/{virus}_coat_protein_cat_align.fasta"
    output:
      ML_tree = "data/tree/{virus}_coat_protein_cat_align.fasta.treefile"
    run:
      shell("iqtree -s %s -pre %s -nt AUTO" % (input.in_align, input.in_align))

####################################################################
# this rule will visualize the information into a dashboard
####################################################################
#rule fasta_temp_hyphy:
#    input:
#      fastas=rules.amino_align.output.outs,
#      trees=rules.build_trees.output.ML_trees
#    output:
#      outs=expand("data/{virus}_coat_protein_cat_align_temp.fasta", virus=viruses)
#    run:
#      import pdb;pdb.set_trace()

####################################################################





