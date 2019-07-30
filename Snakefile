
#import pdb; pdb.set_trace()


## import all functions from python ##
#from python.test import just_print
from python.e_tree import xml_reader
from python.read_json import json_to_fasta


## these are the variables from the grape viruses ##
viruses = ['GLRaV3', 'GPGV', 'GVA']
#viruses = ['GLRaV3']
input_files = ['data/%s/NCBI_data/%s_sequence.gbc.xml' % (virus, virus) for virus in viruses]
            



# rule all: 
#     input:        
#         'data/GLRaV3/NCBI_data/GLRaV3_sequence.gbc.xml'
####################################################################
'''
This rule will read in the XML files from NCBI and parse them into JSONs
'''
rule read_xml:
    params:
        viruses = viruses
    output:
        expand('data/{virus}/{virus}.json', virus=viruses)
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
'''
This rule will read in the JSON from the previous rule and create Fasta files 
for EACH protein represented within each virus
'''
rule read_json:
    params:
        viruses = viruses
    input:
        rules.read_xml.output
    output:
        #"data/sim_seq/{temp}_sim.fasta"
    run:
        zipped = list(zip(input, viruses))
        for i in zipped:
            in_file = i[0]
            virus = i[1]
            json_to_fasta(in_file, virus)
####################################################################
'''
*** WARNING ***
~ this might be an extremely fragile bit of the code ~

This rule might be a little annoying, 
i will need to think of an elegant way to handle this... 
'''
rule cat_files:
    params:
        viruses = viruses
    run:
        for v in viruses:
            print("cat-ing this virus: ",v)
            shell("bash bash/cat_%s.sh" % v)
            print('\n')
####################################################################
'''
This rule will delete old files that 
might have been created from the last run
''' 
rule remove_old_files:
    params:
        viruses = viruses
    run:
        for v in viruses:
            print("removing old runs from this virus: ",v)
            shell("rm -rf data/%s/*.fasta.ckp.gz" % v)
            print('\n')
####################################################################
'''
This rule will run a batch file on 
the nucleotides to put them in frame
and translate them to amino acids 
'''
rule run_hyphy:
    params:
        viruses = viruses
    input:
        v_in_file = "data/{virus}/{virus}_{protein}.fasta"
    output:
        v_out_file = "data/{virus}/{virus}_{protein}_amino.fasta"
    run:
        import pdb; pdb.set_trace()
#     output:
#         "data/hivtrace/{temp}_edge_report.json"
#     shell:
#         "hyphy ../../hyphy-analyses/codon-msa/pre-msa.bf --input ../../data/GLRaV3/GLRaV3_coat_protein_cat.fasta"
####################################################################
'''
This rule will look at the 
need to make sure there are more than X number of sequences to build a tree
'''

# rule check_file_contents:
#     params:
#         viruses = viruses
#     input:
####################################################################

# rule amino_align:
# # #     input:
# # #         "londonMSM_tree_simulator/model1.R"        
# # #     output:

# # #     shell:
# # #         "mafft --amino ../../data/GLRaV3/GLRaV3_coat_protein_cat.fasta_protein.fas > ../../data/GLRaV3/GLRaV3_coat_protein_protein_align.fasta"
####################################################################
# # this rule consumes all the edge reports and creates a table with all the info ##
# rule build_trees:
#     input:
#         expand("data/hivtrace/{temp}_edge_report.json", temp=temp)
#     output:
#         "data/summary_statistics_table.csv"
#     shell:
#         "iqtree -s ../../data/GLRaV3/GLRaV3_coat_protein_protein_align.fasta"
####################################################################
'''
This rule will throw all of the files into a json so that
we can visualize in a dashboard fashion
'''

# rule json_for_dashboard:
####################################################################





