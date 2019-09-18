import re
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

# need to gather nuc_seq #
nuc_seq = "ctgaacaaggccctgcacagaggcgatgtgtacgatactgagctcatagagaaggtcttccccaggagaacaaagaagtgcgtgatccacaaggaactcatagtcaaggatggtcgcgtggactgtgacctggacataatggatgagggcctggacgacatagacgaggtggaattcccgctctatcatgtagggtgcattgtggtggcactgatgccccatggcaagaatctannnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnaaagaaacttgggttgaagacaaatggctcattacgccaagagggtggagataagggcgataatagaagagttggtgctggcgaaagcccagccaactgatgacgcttccgagagcggctacgaccgaactatgtacctgaatactctcttcgggtacatcgccttggtcggtacaagcaaaaaggcggtccactatggggaggtagatatagtaggtcctaaagctagcaaaaagacaggaatagatccgaggggaaagttggtcgtgtcagaactggtgggcaggatgcgcactctgagcgtggcagtcagcgagggacccgtcaagggggcaaccctaaggcagatgtgcgaaccattcgcacagaacgcttacgatttcctcgtactgatggctgagatgggcacgtactcacagttagctaccaagatgactaggtcaggcttcaaggagccacaggttatgttcgactttgcgtcgggcttagatctgaaagcgctgacattgcaagaagctactgtgatacaggctatgcactctcgcctctttcgtacagaaggcgcgaagggggtgttcaacgcccagtcatcagttggcgaacaggctgtcgaaatatagatggatgacccatcgtttctctcgggtaggtccacgtatgctaagcgtaggcgcgctaggcgcatgaatgtgtgtaagtgtggtgctataatgcacaataataaggattgtaaatccagtagtatctctggtcacaaacttgacagattacggttcgtgaaagagggaagagtagccttaacaggcgagactcctgtttaccaaacttggatcgaatgggttcagaccgagtatcatatatatatattagaaacctcagacgatgaggattaatcgtctatcctagctaaggagtaaagtataacttaataataaagcaagct"

# need to gather cds from json #
CDS = ["<1..>234","<335..434","358..954","955..1227"]

new_cds = []
for i in CDS:
    first_temp = i.split("..")[0]
    first = re.findall(r'\d+', first_temp)
    first = [i for j in first for i in j]
    first = "".join(first)
    first = int(first) - 1

    second_temp = i.split("..")[1]
    second = re.findall(r'\d+', second_temp)
    second = [i for j in second for i in j]
    second = "".join(second)
    second = int(second)
    
    cds = (first,second)
    new_cds.append(cds)

'''
acc_num --> static 
 ~ lets enumerate these and add the pos to the protein ~ 
        * duplicates *
list for products --> index with "c"
date (create date and collection date) --> static
country --> static
host --> static 
strain --> static
isolate --> static
'''


acc_num = "123"
products = ["this","that","these","those"]

#trans_1 = "LNKALHRGDVYDTELIEKVFPRRTKKCVVHRELIVKDGRVDCDLDLMDSGLDDVDEDEFPLYHVGCIVVALMPHGKNL"
#trans_2 = "KKLGLKTNGSLRKEGGNEGYHRGVGAGESHPN"
#trans_3 = "MAHCAKKVEMRAIIEELVLAKATPTEDATESGYDRTMYLNTLFGYIALVGTSKKAIHYGEVDIVGPRASKKMGIDPRGKLVVSELVGRMRTLSVAVSEGPVKGATLRQMCEPFAQNAYDFLVLMAEMGTYSQLATKMTRSGFKEPQVMFDFASGLDLKALTLQEATVIQAMHSRLFRTEGAKGVFNAQASVGEQAVEL"
#trans_4 = "MDDPSFLAGRSTYAKRRRARRMNVCRCGAIMHNNKDCKSSSISGHKLDRLRFVKEGRVALTGETPVYRTWVKWVETEYHIYVLETSDDEE"

#new_cds = ["0..20"]
#products = ["some"]

def is_one(acc_num, prod, ):
    header = "%s_%s" % (acc_num, products[0])
    return header



'''
want to grab:
    1. full gene
    2. pre-overlapping portion
    3. overlapping portion
    4. post-overlapping portion 
'''
with open("test.fasta", "w") as out:
    print("there is/are ", len(new_cds), " ORF(s) here")
    print("these are the CDSs: ", new_cds)
    
    # when there is only one element in the CDS, just print it #
    if len(new_cds) == 1:
        out.write(">{}\n{}\n".format(is_one(acc_num, products),nuc_seq))
    
    # otherwise #
    else:
        print(len(new_cds))
        print(range(len(new_cds)))
        

        print("~ Checking for overlapping ORFs ~")
        # just writing full ORF here #
        for c, item_1 in enumerate(new_cds):
            base_header = "%s_%s" % (acc_num, products[c])
            orf1_s, orf1_e = new_cds[c][0], new_cds[c][1] 
        
            header = base_header + "_orf" + str(c+1) + "_full"
            seq = nuc_seq[orf1_s: orf1_e]
            out.write(">{}\n{}\n".format(header,seq))

            # now check for overlaps #
            for i, item_2 in enumerate(new_cds):
                '''
                this way we are checking:
                1 -> 2,3,4
                2 -> 3,4
                3 -> 4
                '''
                if c < i and c < len(new_cds):
                    print("checking ORF",c+1, " to ORF",i+1)
                    #print("this is i: ", i)
                    orf2_s, orf2_e = new_cds[i][0], new_cds[i][1]
                    print("Next ORF to Compare ", new_cds[i])
                    #print("This is ORF",orf1_e, " end", "this is ORF",orf2_s, " start")


                    r = orf1_e - orf2_s
                    #print("this is r: ", r)
                    if r > 0:
                        '''
                        There are three parts of the sequence that need to be written here:
                            1. pre-overlap
                            2. overlap
                            3. post-overlap
                        ~ for printing in header (c+1) is the ORF, (c+2) is the next ORF ~
                        '''
                        info = " ** found an overlap between orf" + str(c+1) + " and orf" + str(i+1) + " **"
                        print(info)
                        
                        ## have a non of first ##
                        non_header_orf1 = "_orf" + str(c+1) + "_non"
                        header = base_header + non_header_orf1
                        seq = nuc_seq[orf1_s: orf1_s + (r-1)]
                        out.write(">{}\n{}\n".format(header,seq))

                        ## have an overlap ##
                        overlap_header = "_orf%d_%s_orf%d_overlap" % (c+1, products[c+1], c+2)
                        header = base_header + overlap_header
                        seq = nuc_seq[orf2_s: orf2_s + r]
                        out.write(">{}\n{}\n".format(header,seq))

                        ## have a non overlap second ##
                        '''
                        need to add logic to:
                        1. check the overlap of the next of the next ORF to 
                        make sure there are no more overlaps to watch out for 
                        before writing it to a file
                        '''
                        
                        # if you are NOT penultimate index #
                        if c+2 < len(new_cds):
                            next_orf = c+2
                            
                            print("these are the amount of indicies left to compare: ", len(new_cds) - next_orf)
                                
                                
                                #orf_next_s = new_cds[next_orf][0]
                                #r_next = orf2_e - orf_next_s
                            
                                #print("this is c ", c, " and these are then next ORFs to check", orf_next_s)
                                #print("this is r_next ", r_next)
                            
                                # NOT penultimate but DO have overlap #
                                #if r_next > 0:
                                    #print("I am not the pen and DO have another overlap")
                                
                                
                                # NOT penultimate and DO NOT overlap #
                                #else:
                                    #print("I am not the pen and DO NOT have another overlap")

                            non_header_orf2 = "_orf" + str(c+2) + "_non"
                            header = base_header + non_header_orf2
                            seq = nuc_seq[orf2_s + r: orf2_e]
                            out.write(">{}\n{}\n".format(header,seq))
                        
                        # if you are penultimate, just
                        else:
                            print("I am pen")


                        print("\n")

                    else:
                        continue 
            
            print("\n") 




