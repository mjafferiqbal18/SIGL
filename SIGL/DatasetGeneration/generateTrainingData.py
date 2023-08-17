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

    for node in graph:
        # Handling nodes
        if "id" in node:
            if node['type'] == "Artifact":
                try:
                    hashNames[node['id']] = node['annotations']['path']
                    process[node['id']] = 0
                except:
                    exclude.append(node["id"])
            if node['type'] == "Process":
                hashNames[node['id']] = node['annotations']['exe']
                process[node['id']] = 1
        # Handling edges        
        else:
            if node['to'] in exclude or node['from'] in exclude:
                tempEdges.append((node['to'],node['from']))
            else:
                if node["to"] != node["from"]:    
                    edges.append((node['to'],node['from']))

   

    for node in exclude:
      
        pre = []
        post = []
        for l,r in tempEdges:
            if l == node:
                post.append(r)
            if r == node:
                pre.append(l)                   
        for i in pre:
            for j in post:
                edges.append((i,j))



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
