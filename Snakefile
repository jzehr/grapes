
#import pdb; pdb.set_trace()


## import all functions from python ##
#from python.test import just_print
from python.e_tree import xml_reader


## these are the variables from the grape viruses ##
viruses = ['GLRaV3', 'GPGV', 'GVA']
input_files = ['data/%s/NCBI_data/%s_sequence.gbc.xml' % (virus, virus) for virus in viruses]
            



# rule all: 
#     input:        
#         'data/GLRaV3/NCBI_data/GLRaV3_sequence.gbc.xml'


## this rule that will use the python script to make and write matrices to .ibf files ## 
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


# ## this rule will take the matrices and input them into the sim_seq.bf to make fasta files ##
#rule read_json:
#     input:
#         os.path.join(os.getcwd(), "data/matrix/{temp}_nodes.ibf")
#     output:
#         "data/sim_seq/{temp}_sim.fasta"
#     shell:  
#         "HYPHYMP simulate/SimulateSequence.bf {input} > {output}"


## This rule might be a little annoying, i will need to think of an elegant way to handle this... ##
#rule cat_files:
#     input:
#         rules.seq_gen.output
#     output:
#         "data/hivtrace/{temp}_nodes.results.json"
#     shell:
#         "hivtrace -i {input} -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

## this rule will take the generated fasta files and input them into HIVtrace 
#rule remove_old_files:
#     input:
#         rules.seq_gen.output
#     output:
#         "data/hivtrace/{temp}_nodes.nofilter.results.json"
#     shell:
#         "hivtrace -i {input} -a resolve -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

# rule run_hyphy:
# #     input:
# #         with_edge_filtering=rules.hiv_trace_with_edge_filtering.output,
# #         with_out_edge_filtering=rules.hiv_trace_without_edge_filtering.output
# #     output:
# #         "data/hivtrace/{temp}_edge_report.json"
# #     run:
# #         transmission_chains=[matrix_maker(INTERNAL_LENGTH,TIP_LENGTH,int(n.split('/')[2].split('_')[0])) for n in input.with_edge_filtering]
# #         pairs = zip(input.with_edge_filtering, input.with_out_edge_filtering, transmission_chains, output)
# #         for p in pairs:
# #             edge_report(*p)


# rule amino_align:
# # #     input:
# # #         "londonMSM_tree_simulator/model1.R"        
# # #     output:

# # #     script:
# # #         "{input}"

# # this rule consumes all the edge reports and creates a table with all the info ##
# rule build_trees:
#     input:
#         expand("data/hivtrace/{temp}_edge_report.json", temp=temp)
#     output:
#         "data/summary_statistics_table.csv"
#     run:
#         sum_stats_table(input, output, sims)









