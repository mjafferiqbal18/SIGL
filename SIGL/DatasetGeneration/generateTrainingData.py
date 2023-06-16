import os
import json
import sys


def processSPADEJSON(fileName,executableName):

    with open(fileName) as line:
        graph = json.load(line)

    edges = [] # Edges in the graph represented as a list of tuples
    tempEdges = [] 
    hashNames = {} # Maps hash of each node to it's path name
    process = {} # Stores if a node is a process or artifact
    exclude = [] # Used to remove all non compatible Artifacts e.g. unix sockets

    for i in graph:

        if "id" in i:
            if i['type'] == "Artifact":
                try:
                    hashNames[i['id']] = i['annotations']['path']
                    process[i['id']] = 0
                except:
                    exclude.append(i["id"])
            if i['type'] == "Process":
                hashNames[i['id']] = i['annotations']['exe']
                process[i['id']] = 1
        else:
                tempEdges.append((i['to'],i['from']))


    def numParents(node):
        counter = 0
        for i in tempEdges:
            if i[0] == node and i[1] not in exclude:
                counter = counter + 1
        if counter > 0:
            return False
        else: 
            return True 
        
    stop = False
    while stop == False:
        stop = True
        for i in tempEdges:
            if i[1] in exclude and i[0] not in exclude and numParents(i[0]) == True:
                exclude.append(i[0])
                stop = False   


    for i in exclude:
        if i in hashNames.keys():
            hashNames.pop(i)
        if i in process.keys():
            process.pop(i)    


    for i in hashNames.keys():
        for j in tempEdges:
            if i == j[1] and j[0] not in exclude:
                edges.append((j[0],j[1]))

    jsonDict = {
        "name": fileName,
        "exe": executableName,
        "edges": edges,
        "hash": hashNames,
        "types": process 
    }

    return jsonDict





def generateDataset():

    directory = f"./graphs/{sys.argv[1]}"
    executableName = sys.argv[2]

    jsonDict = processSPADEJSON(directory,executableName)

    try:
        with open('dataset.json', 'r') as f:
            output_list = json.load(f)
    except json.decoder.JSONDecodeError:
        output_list = []

    
    output_list.append(jsonDict)   


    with open("dataset.json", "w") as f:
        f.write("[\n")
        f.write(json.dumps(output_list[0]))
        if len(output_list) > 1:
            for obj in output_list[1:]:
                f.write(",\n" + json.dumps(obj))
        f.write("\n]")


if len(sys.argv) >= 3:
    generateDataset()