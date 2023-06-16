import json
import random
import sys
import numpy as np


def walks(graph):    


    visited = []

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
    def randomWalk(length, frequency,exe):
        source = findHash(exe)
        first = True
        nodes = list(graph["hash"].keys())
        frequency = len(nodes)
        result = []
        for i in range(frequency):
            sentences = []
            if first == False:
                ran = random.randint(0,len(nodes)-1)
                while len(getAllChildren(nodes[ran])) == 0:
                    ran = random.randint(0,len(nodes)-1)
                currentNode = nodes[ran]
            else:
                currentNode = source
                first = False        
            try:
                for j in range(length):
                    if currentNode not in visited:
                        visited.append(currentNode)
                    path = getPath(currentNode)
                    sentences.extend(path)
                    ancestors = getAllChildren(currentNode)
                    currentNode = ancestors[random.randint(0,len(ancestors)-1)]
            except:
                pass        
            result.append(sentences)         
        return result        


    return randomWalk(15,30,graph["exe"])


def generateWalks():


    paths = list()
    with open("SIGL/DatasetGeneration/dataset.json") as line:
        dataset = json.load(line)


    for graph in dataset:
        paths.append(walks(graph))
            
    with open("SIGL/NodeEmbeddings/Dataset.txt", "w") as f:
        for i in paths:
            for s in i:
                f.write(" ".join(s))
                f.write('\n')
    
   

         