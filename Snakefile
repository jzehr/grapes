
#import pdb; pdb.set_trace()


## import all functions from python ##
#from python.test import just_print
from python.json_part_list import list_maker
from python.flat import flatten
from python.e_tree import xml_reader
from python.read_json import json_to_fasta


## these are the variables from the grape viruses ##
#viruses = ['GLRaV3', 'GPGV', 'GVA']
viruses = ['GLRaV3']

# parts = {GLRaV3 : ['55_KDa_protein', 'p_protease__methyl_transferase__helicase', 'RNA-dependent_RNA_polymerase', '6_kDa_protein', '5_kDa_protein', '59_kDa_protein', '55_kDa_protein', '35_kDa_coat_protein', '53_kDa_protein', '21_kDa_protein', '19.6_kDa_protein', '19.7_kDa_protein', '4_kDa_protein', '7_kDa_protein', 'polymerase', 'RNA_dependent_RNA_polymerase', 'HSP70-like_protein', 'coat_protein', 'heat_shock_protein_70_homologue', 'ORF1a', 'heat_shock_protein_70-like_protein', 'major_coat_protein', 'RNA_polymerase', 'RNA-dependent_RNA_polymerase_2', '59.3_kDa_protein', '55.1_kDa_protein', 'methyl_transferase__helicase', 'Hsp70-like_protein', 'Hsp90-like_protein', 'divergent_coat_protein', 'polyprotein', 'HSP70h', '53_kDa_coat_protein_divergent', 'heat_shock_protein', 'no_value', 'movement_protein', 'heat_shock_70-like_protein', 'Heat_shock_protein_70_homolog', 'heat_shock_protein_70', 'capsid_protein', 'HSP90-like_protein', 'p5', 'p55', 'CPm', 'p21', 'p19.6', 'p19.7', 'p4', 'p7', 'methyl_transferase', 'hypothetical_protein', '245_kDa_polyprotein', 'HSP90h', 'coat_protein_divergent', '3.9_kDa_protein', 'p19.7_RNA_silencing_suppressor_protein', 'replication_associated_protein_3', 'p6', 'Hsp70h', 'Hsp90h', 'CP', 'dCP', 'heat_schock_protein_70-like_protein', 'heat_shock_protein_90', 'diverged_copy_of_the_GLRaV-3_coat_protein', 'Papain-like_protease___methyl_transferase___AlkB_and_helicase_domains', 'divergent_(minor)_coat_protein', '19.8_kDa_protein', 'heat_shock_protein_hsp70h', 'methyltransferase__helicase', 'methyltransferase__helicase_protein', 'ORF7_protein', 'methyltransferase', '19.3_kDa_protein', '9_kDa_protein', '6.2_kDa_protein', 'RdRp', '5.5_kDa_protein', 'divergent_capsid_protein', '20_kDa_protein', '19_kDa_protein', '19.5_kDa_protein', 'RNA_dependent_RNA_polmerase', 'small_hydrophobic_protein', 'hsp70-like_protein', 'capsid_protein_divergent', 'p20', 'truncated_p6', 'replication-related_polyprotein', 'major_capsid_protein', 'p20A', 'p20B', 'putative_small_protein', 'p20_protein'], \
# GPGV : ['movement_protein', 'coat_protein', 'RNA_dependent_RNA_polymerase', 'polyprotein', 'capsid_protein', 'RNA-dependent_RNA_polymerase', 'replicase', 'no_value', 'rdRpol', 'MP', 'CP', 'RdRp'],\
#  GVA : ['coat_protein', 'RNA-dependent_RNA_polymerase', 'unknown', 'movement_protein', 'nucleic_acid_binding_protein', 'ORF5', 'capsid_protein', 'replicase', '19_kDa_protein', '10_kDa_protein', 'putative_replicase', 'RNA_binding_protein', '194_kDa_protein', 'RNA-binding_protein', 'replication-related_protein', 'RNA_silencing_suppressor', 'replication-like_protein', 'replication_protein', 'silencing_suppressor', 'truncated_coat_protein', 'mutant_silencing_suppressor', 'truncated_silencing_suppressor', 'no_value', '195_kDa_replicase', 'MP', 'CP', 'hypothetical_protein', 'putative_movement_protein', 'putative_RNA_binding_protein', 'replicase_protein', 'putative_19_kDa_protein', 'GVA_19kDa_protein', 'RNA-binding_protein__silencing_suppressor']}

input_files = ['rsrc/%s/NCBI_data/%s_sequence.gbc.xml' % (v, v) for v in viruses]



'''
this will collect all the parts of proteins
want to put in the virus config file and get out a list of associated proteins
then add all those lists together to make 'temp'
'''
all_virus = []
for v in viruses:
    temp_file = 'rsrc/virus_%s_config.json' % v
    all_virus.append(list_maker(temp_file, v))
# print(flatten(all_virus))
all_virus = flatten(all_virus)



####################################################################
# rule all: 
#     input:        
#         'data/GLRaV3/NCBI_data/GLRaV3_sequence.gbc.xml'
####################################################################

####################################################################
'''
This rule will read in the XML files from NCBI and parse them into JSONs
'''
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
'''
This rule will read in the JSON from the previous rule and create Fasta files 
for EACH protein represented within each virus
'''
####################################################################
rule json_to_fasta:
    params:
        all_virus=all_virus
    input:
        virus_xml = rules.xml_to_json.output
    output:
        #"data/{virus}/{temp}.fasta"
        all_outs = expand("data/{temp}.fasta" , virus=viruses, temp=all_virus)
        #"data/sim_seq/{temp}_sim.fasta"
    run:
        #import pdb;pdb.set_trace()
        json_to_fasta(input.virus_xml, output.all_outs)

####################################################################
'''
*** WARNING ***
~ this might be an extremely fragile bit of the code ~

This rule might be a little annoying, 
i will need to think of an elegant way to handle this... 
'''
####################################################################
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
####################################################################
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
####################################################################
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
####################################################################

####################################################################
'''
'''
# rule check_file_contents:
#     params:
#         viruses = viruses
#     input:
####################################################################

####################################################################
'''

'''
####################################################################
# rule amino_align:
# # #     input:
# # #         "londonMSM_tree_simulator/model1.R"        
# # #     output:

# # #     shell:
# # #         "mafft --amino ../../data/GLRaV3/GLRaV3_coat_protein_cat.fasta_protein.fas > ../../data/GLRaV3/GLRaV3_coat_protein_protein_align.fasta"

####################################################################
'''
this rule consumes all the edge reports and creates a table with all the info 
'''
####################################################################
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
####################################################################
# rule json_for_dashboard:


####################################################################





