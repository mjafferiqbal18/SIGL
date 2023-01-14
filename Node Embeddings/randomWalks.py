import json
import random

with open("onedrive-test.json") as line:
    graph = json.load(line)


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
    for i in graph:
        if "id" in i and i['id'] == node:
            if "path" in i["annotations"]:
                return splitComponents(i["annotations"]["path"])
            if "exe" in i["annotations"]:
                return splitComponents(i["annotations"]["exe"])

# Helper function for getPath, splits a given path into indiviual components
def splitComponents(pathName):
    componentList = pathName.split("/")
    componentList.pop(0)
    return componentList


# Will generate walks of specified number and a specified length
def randomWalk(length,frequency,source):
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




print(randomWalk(3,3,"8e32b7592087fda577926f02d1966afe"))