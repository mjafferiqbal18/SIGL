import json
import random
import sys
#import gensim

with open("onedrive-test.json") as line:
    graph = json.load(line)


# if len(sys.argv) > 2:
#     print("Error:you can only pass one argument")

def generatePairs():
    pair = dict()
    for i in graph:
        if "id" in i:
            if i['type'] == "Artifact":
                pair[i['annotations']['path']] = i['id']
            if i['type'] == "Process":
                pair[i['annotations']['exe']] = i['id']
        else:
            break
    return pair

nodes = generatePairs()


def findHash(nodeName):
    if nodeName in nodes:
        return nodes[nodeName]
    else:
        sys.exit("Executable does not exist")                   


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
    for path,hash in nodes.items():
        if hash==node:
            return splitComponents(path)


# Helper function for getPath, splits a given path into indiviual components
def splitComponents(pathName):
    componentList = pathName.split("/")
    componentList.pop(0)
    return componentList


# Will generate walks of specified number and a specified length
def randomWalk(length,frequency,exe):
    source = findHash(exe)
    result = []
    for i in range(frequency):
        sentences = []
        currentNode = source
        for j in range(length):
            sentences.extend(getPath(currentNode))
            ancestors = getAllChildren(currentNode)
            currentNode = ancestors[random.randint(0,len(ancestors)-1)]
        result.append(sentences)    
    return result        




print(randomWalk(3,3,sys.argv[1]))