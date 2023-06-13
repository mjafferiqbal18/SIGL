import json
import random
import sys
import numpy as np


def walks(graph):    
    print(graph["name"])

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
            try:
                for j in range(length):
                    path = getPath(currentNode)
                    sentences.extend(path)
                    ancestors = getAllChildren(currentNode)
                    currentNode = ancestors[random.randint(0,len(ancestors)-1)]
            except:
                pass        
            result.append(sentences)    
        return result        



    return randomWalk(50,30,graph["exe"])


def generateWalks():
    paths = list()
    with open("SIGL/DatasetGeneration/dataset.json") as line:
        dataset = json.load(line)


    for graph in dataset:
        paths.append(walks(graph))


    with open("SIGL/NodeEmbeddings/ALaCarte/Dataset.txt", "w") as f:
        for i in paths:
            for s in i:
                f.write(" ".join(s))
                f.write('\n')
