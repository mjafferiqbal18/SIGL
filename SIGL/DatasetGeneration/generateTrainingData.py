import os
import json
import sys

fileName = sys.argv[1]
directory = f"./graphs/{sys.argv[1]}"
executableName = sys.argv[2]
data = []


with open(directory) as line:
    graph = json.load(line)

edges = list()
hashnames = dict()
process = dict()


exclude = []
for i in graph:

    if "id" in i:
        if i['type'] == "Artifact":
            if i["annotations"]["subtype"] == "file" or i["annotations"]["subtype"] == "link":
                hashnames[i['id']] = i['annotations']['path']
                process[i['id']] = 0
            else:
                exclude.append(i["id"])
        if i['type'] == "Process":
            hashnames[i['id']] = i['annotations']['exe']
            process[i['id']] = 1
    else:
        if i['to'] not in exclude and i["from"] not in exclude:
            edges.append((i['to'],i['from']))
        


json_dict = {
    "name": fileName,
    "exe": executableName,
    "edges": edges,
    "hash": hashnames,
    "types": process 
}


try:
    with open('dataset.json', 'r') as f:
        output_list = json.load(f)
except json.decoder.JSONDecodeError:
    # If the file is empty or not a valid JSON object, create a new empty array
    output_list = []

   
output_list.append(json_dict)   


with open("dataset.json", "w") as f:
    f.write("[\n")
    f.write(json.dumps(output_list[0]))
    if len(output_list) > 1:
        for obj in output_list[1:]:
            f.write(",\n" + json.dumps(obj))
    f.write("\n]")


