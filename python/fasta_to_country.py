import json
import csv 



def country(in_f, out_fs, countries):
    in_file = str(in_f)
    outs = list(out_fs)
    countries = list(countries)


    with open(in_file) as json_f:
        data = json.load(json_f)

        keys = list(data.keys())
        for pos, item in enumerate(outs):
            country = countries[pos]
            print(country)
            #with open(str(item), "w") as out:
                #for p in keys:
                    #if data[p]
    

