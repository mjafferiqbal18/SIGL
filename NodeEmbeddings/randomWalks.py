import json
import random
import sys
import numpy as np

paths = list()
with open("../DatasetGeneration/dataset.json") as line:
    dataset = json.load(line)


for graph in dataset:

    # Given a node, this function will return the hash id of all its children nodes 
    def getAllChildren(node):
        pathsList = []
        for i in graph["edges"]:
            if i[1] == node:
                if i[0] not in pathsList:
                    pathsList.append(i[0])
        return pathsList


    # Given a node, this function will return the components of its path
    def getPath(node):
        for hash,path in graph["hash"].items():
            if hash==node:
                return splitComponents(path)


    # Helper function for getPath, splits a given path into indiviual components
    def splitComponents(pathName):
        componentList = pathName.split("/")
        componentList.pop(0)
        return componentList


    def findHash(path):
        for i in graph["hash"]:
            if graph["hash"][i] == path:
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



    paths.append(randomWalk(3,3,graph["exe"]))



with open("./ALaCarte/Dataset.txt", "w") as f:
    for i in paths:
        for s in i:
            f.write(" ".join(s))
            f.write('\n')
