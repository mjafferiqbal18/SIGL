import os
import json
import sys


def processSPADEJSON(fileName,directory):

    with open(directory) as line:
        graph = json.load(line)

    edges = [] # Edges in the graph represented as a list of tuples
    hashNames = {} # Maps hash of each node to it's path name
    process = {} # Stores if a node is a process or artifact
    
    for node in graph:
        # Handling nodes
        if "id" in node:
            if node['type'] == "Artifact":
                try:
                    hashNames[node['id']] = node['annotations']['path']
                    process[node['id']] = 0
                except:
                    hashNames[node['id']] = node['annotations']['subtype'].replace(" ", "")
                    process[node['id']] = 0
            if node['type'] == "Process":
                hashNames[node['id']] = node['annotations']['exe']
                process[node['id']] = 1
        # Handling edges
        else:
            if node["to"] != node["from"]:  #Remove self edge
                edges.append((node['to'],node['from']))

    jsonDict = {
        "name": fileName,
        "edges": edges,
        "hash": hashNames,
        "types": process
    }

    return jsonDict





def generateDataset():

    base = os.path.dirname(os.path.abspath(__file__))
    trainingDir = os.path.join(base,"trainingGraphs")

    graphsList = os.listdir(trainingDir)

    outputList = []

    for graph in graphsList:

        graphName = graph.split("-")

        directory = os.path.join(trainingDir, graph)

        jsonDict = processSPADEJSON(graphName[0]+graphName[1][0],directory)

        outputList.append(jsonDict)

 
    with open(os.path.join(base, "trainingDataset.json") , "w") as f:

        f.write("[\n")
        f.write(json.dumps(outputList[0]))
        if len(outputList) > 1:
            for obj in outputList[1:]:
                f.write(",\n" + json.dumps(obj))
        f.write("\n]")
