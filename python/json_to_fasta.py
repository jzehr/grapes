import json


def fasta_maker(inf, outf, imp_virs):
    in_f = str(inf)
    out_f = str(outf)

    print("this is in --> ", in_f, "this is out --> ", out_f)
    print(imp_virs)

    def name_fixer(string):
        new = []
        bad_chars = [' ',',','.','/','-','(',')',':']
        def checker(char):
            if char in bad_chars:
                return "_"
            else:
                return char
        for char in list(string):
            new.append(checker(char))
        temp = "".join(new)
        name = temp.replace("__","_")
        return name

        '''
        1. need to grab nuc seq,
        2. CDS (and make sure there are the same number as proteins or at least the trans seqs
        3. grab indexed seqs and handle overlaps
        4. print those to a file
        '''
    
    seq = ""
    with open(in_f, "r") as j_file:
        data = json.load(j_file)
        keys = list(data.keys())
        print(keys)
        #for key in keys:
         #   print(data[key])



