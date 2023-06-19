import os
import json
import sys


def processSPADEJSON(fileName,directory,executableName):

    with open(directory) as line:
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

    graphs = os.listdir("SIGL/DatasetGeneration/graphs")

    execmap = {"7zip":"/usr/bin/p7zip", "onedrive":"/usr/bin/onedrive", "skype": "usr/bin/skypeforlinux", "teamviewer":"usr/bin/teamviewer","winrar":"usr/bin/rar","filezilla":"usr/bin/filezilla","shotcut":"/usr/lib/shotcut","pwsafe":"/usr/bin/pwsafe","firefox":"/usr/bin/firefox","dropbox":"/usr/bin/dropbox"}

    output_list = []

    for i in graphs:
        graphName = i.split("-")
        print(graphName[0],graphName[1][0])
        directory = f"SIGL/DatasetGeneration/graphs/{i}"
        executableName = execmap[graphName[0]]
            
        jsonDict = processSPADEJSON(graphName[0]+graphName[1][0],directory,executableName)

        output_list.append(jsonDict)   


    with open("SIGL/DatasetGeneration/dataset.json", "w") as f:
        f.write("[\n")
        f.write(json.dumps(output_list[0]))
        if len(output_list) > 1:
            for obj in output_list[1:]:
                f.write(",\n" + json.dumps(obj))
        f.write("\n]")
