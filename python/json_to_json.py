import json

'''
this will grab information from the MASTER
JSON file and parse it into separate JSON files
for each virus
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

        keys = list(data.keys())

        with open(out_f, "w") as out:
            for key in data:
                temp_target = data[key]["organism"]
                target = [i for j in temp_target for i in j]
                target = "".join(target)

                target = name_fixer(target)

                if target == virus:
                    print("finding target --> ", target)
                    payload = {}

                    payload.update(data[key])

                    #print(payload)
                    json.dump(payload, out, indent=4)


