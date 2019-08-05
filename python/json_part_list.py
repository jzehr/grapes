import json

def list_maker(virus_json, virus):
    virus_json = str(virus_json)
    virus = str(virus)

    with open(virus_json) as in_f:
        data = json.load(in_f)
        for p in data.items():
            payload = [virus+"_"+i for i in p[1]]
            return payload
