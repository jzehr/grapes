import json

'''
check for virus in master, 
save it to a dict 
print that in json format to outf
'''

def virus_json(input_full, virus, out_file):
    in_f = str(input_full)
    virus = str(virus)
    out_f = str(out_file)

    
    def name_fixer(string):
        new = []
        bad_chars = [' ',',','.','/','-','(',')',':']
        def checker(char):
            if char in bad_chars:
                return '_'
            else:
                return char
        for char in list(string):
            new.append(checker(char))
        temp = "".join(new)
        name = temp.replace("__","_")
        return name
   

    with open(in_f, "r") as j_file:
        data = json.load(j_file)
        ## data is a dictionary ##
        
        keys = list(data.keys())
        #print(keys)

        payload = {}
        for key in keys:
            temp = data[key]["organism"]
            t = [i for j in temp for i in j]
            name = "".join(t)
            if name_fixer(name) == virus:
                info = {}
                info[key] = data[key]
                payload.update(info)

        with open(out_f, "w") as out:
            json.dump(payload, out, indent=4)



