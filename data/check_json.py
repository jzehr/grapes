import json


json_f = "temp.json"

with open(json_f, "r") as in_f:
    data = json.load(in_f)
    for d in data:
        print(d)

