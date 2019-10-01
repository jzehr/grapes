from Bio import SeqIO


from python.helper import name_fixer


def region_fasta(input_fas, output_fas, regions):

    input_fas = str(input_fas)
    out_fas = output_fas
    

    data = []
    for record in SeqIO.parse(input_fas, "fasta"):
        data.append((str(record.id), record.seq))
    
    for pos, item in enumerate(regions):
        
        with open(out_fas[pos], "w") as out:
            key_word = item.split("-")[0].lower()
            for d in data:
                if key_word in d[0].lower():
                    out.write(">{}\n{}\n".format(d[0],d[1])) 


