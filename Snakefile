
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

input_files = ['rsrc/%s/NCBI_data/%s_sequence.gbc.xml' % (v, v) for v in viruses]




#this will read in the virus config files and scrape all the protein parts
#that come from that virus

#example: heat schock protein 70-like protein

all_virus = []
for v in viruses:
    temp_file = 'rsrc/virus_%s_config.json' % v
    all_virus.append(list_maker(temp_file, v))
# print(flatten(all_virus))
all_virus = flatten(all_virus)



####################################################################
# rule all: 
#     input:        
#         'data/dashboard.json'
####################################################################

####################################################################
# This rule will read in the XML files from NCBI and parse them into JSONs
####################################################################
rule xml_to_json:
    params:
        viruses = viruses
    output:
        expand('rsrc/{virus}/NCBI_data/{virus}.json', virus=viruses)
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
    params:
        all_virus=all_virus
        # viruses=viruses
    input:
        virus_xml = rules.xml_to_json.output
    output:
        all_outs = expand("data/{temp}.fasta" , temp=all_virus)
    run:
        #import pdb;pdb.set_trace()
        json_to_fasta(input.virus_xml, output.all_outs, viruses)

####################################################################
#               *** WARNING ***
# ~ this might be an extremely fragile bit of the code ~
# 
# This rule might be a little annoying, 
# i will need to think of an elegant way to handle this... 
####################################################################
rule cat_files:
    # params:
    #     viruses = viruses
    input:
        in_files=rules.json_to_fasta.output.all_outs
    output:
        outs_temp = expand("data/{virus}_coat_protein_temp_cat.fasta" , virus=viruses)
        # outs_cat = expand("data/{virus}_coat_protein_cat.fasta" , virus=viruses)
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
        outs_cat = expand("data/{virus}_coat_protein_cat.fasta" , virus=viruses)
    run:
        zipped = list(zip(viruses, input.in_files, output.outs_cat))
        for z in zipped:
            virus = z[0]
            temp_file = z[1]
            out_file = z[2]
            # print(virus, temp_file, out_file)
            with open(temp_file, "r") as in_put:
                with open(out_file, "w") as out_put: 
                    for pos, line in enumerate(in_put):
                        # print(pos, [line])
                        bad_1 = 'MGAYTHVDFHESRLLKDKQDYLSFKSANEAPPDPPGYVRPDSYVRAYLIQRADFPNTQSLSVTLSVASNKLASGLMGSDAVSSSFMLMNDAGDYFECGVCHNKPYLGREVIFCRKYIGGRGVEITTGKNYTSNNWNETSYVIQVNVVDGLAQTTVNSTYTQTDVSGLPKNWTRIYKITKIVSVDQNLYPGCFSDSKLGVMRIRSLLVSPVRIFFRGILLKPLKKSFNARIEDVLNIDDTSLLEPSPVVPESTGGVGPSEQLDVVALTSDVTELINTRGQGKICFPDSVLSINEADIYDERYLPITEALQINARLRRLVLSKGGSQTPRDMGNMIVAMIQLFVLYSTVKNISVKDGYRVETELGQKKVYLSYSEVREAILGGKYDASPTNTVRSFMRYFTHTTITLLIEKKIQPAYTALAKHGVPKRFTPYCFDFALLDNRYYPADVLKANAMACAIAIKSANLRRKGSETYNILESI\n'
                        bad_2 = '>QCY41301.1_coat_protein_MK804765.1_Brazil_19-Mar-2018_Vitis-sp.-cv.-BRS-Nubia-(hybrid-grapevine)_\n'
                        if bad_1 == line or bad_2 == line: 
                            continue 
                        out_put.write(line)

####################################################################
# This rule will run a batch file on 
# the nucleotides to put them in frame
# and translate them to amino acids 
#
# ** do we even need this rule anymore?? ** 
#
####################################################################
# rule run_hyphy:
#     params:
#         viruses = viruses
#     input:
#         v_in_file = "data/{temp}_cat.fasta"
#     run:
#         for infile in v_in_file:
#         shell("hyphy hyphy-analyses/codon-msa/pre-msa.bf --infile %s" % infile)

####################################################################
# This rule will look at the number of sequences in a fasta file 
# * need to make sure there are more than X number of sequences to *
# * continue down the pipeline *
# mark down which ones only have one or two seqs
####################################################################
# rule check_file_contents:
#     params:
#         viruses = viruses
#     input:


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
        ins = rules.amino_align.output.outs
    run:
       # shell("rm data/*.fasta.*")
        for file in input.ins:
            shell("iqtree -s %s -nt AUTO" % file)

####################################################################
# this rule will visualize the information into a dashboard
####################################################################
# rule json_for_dashboard:


####################################################################





