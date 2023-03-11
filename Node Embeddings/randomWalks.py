import json
import random
import sys
import numpy as np


with open(sys.argv[1]) as line:
    graph = json.load(line)

edges = list()
def generatePairs():

    pair = dict()
    for i in graph:
        if "id" in i:
            if i['type'] == "Artifact":
                pair[i['id']] = i['annotations']['path']
            if i['type'] == "Process":
                pair[i['id']] = i['annotations']['exe']
        else:
            edges.append((i['to'],i['from']))
    return pair

nodes = generatePairs()

                  


# Given a node, this function will return the hash id of all its children nodes 
def getAllChildren(node):
    pathsList = []
    for i in graph:
        if "from" in i and i["from"] == node:
            if i["to"] not in pathsList:
                pathsList.append(i["to"])
    return pathsList

# Given a node, this function will return the components of its path
def getPath(node):
    for hsh,path in nodes.items():
        if hsh==node:
            return splitComponents(path)


# Helper function for getPath, splits a given path into indiviual components
def splitComponents(pathName):
    componentList = pathName.split("/")
    componentList.pop(0)
    return componentList


def findHash(path):
    for i in nodes:
        if nodes[i] == path:
            return i




# Will generate walks of specified number and a specified length
def randomWalk(length,frequency,exe):
    source = findHash(exe)
    result = []
    for i in range(frequency):
        sentences = []
        currentNode = source
        for j in range(length):
            path = getPath(currentNode)
            sentences.extend(path)
            ancestors = getAllChildren(currentNode)
            currentNode = ancestors[random.randint(0,len(ancestors)-1)]
        result.append(sentences)    
    return result        




#print(randomWalk(3,3,sys.argv[2]))

walk_paths = randomWalk(3,3,sys.argv[2])




print(walk_paths)

with open("Dataset.txt", "a") as f:
    for s in walk_paths:
        f.write(" ".join(s))
        f.write('\n')
