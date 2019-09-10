import json

'''
this will grab information from the MASTER
json file and parse it into separate fasta files
for each virus
'''

def fasta_maker(input_full, virus, out_file):
    in_f = str(input_full)
    virus = str(virus)
    out_f = str(out_file)

    print("I am starting")
    temp_virus = virus.replace("_"," ")
    with open(in_f, "r") as j_file:
        data = json.load(j_file)

        keys = list(data.keys())

        print(keys)
        for key in data:
            temp_target = data[key]["organism"]
            target = [i for j in temp_target for i in j]
            target = "".join(target)
            print(target)
            #print(target, temp_virus)

            if target == temp_virus:
                print(target, temp_virus)

            #print(item)
    #print(in_f, virus, out_f)
