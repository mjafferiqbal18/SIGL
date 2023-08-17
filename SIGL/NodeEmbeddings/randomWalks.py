import json
import random


# Given a node, this function will return the components of its path
def getPath(node,graph):
    for hash,path in graph["hash"].items():
        if hash==node:
            return splitComponents(path)


# Helper function for getPath, splits a given path into indiviual components
def splitComponents(pathName):
    componentList = pathName.split("/")
    componentList.pop(0)
    return componentList



# Will generate walks of specified number and a specified length
def randomWalk(length, frequency,graph):
    
    visited = [] 
    children = {} # Contains a list of all children for each node

    for i in graph["edges"]:
        if i[0] in children:
            children[i[0]].append(i[1])
        else:
            children[i[0]] = [i[1]]    

    nodes = list(graph["hash"].keys()) 
    result = []
    counter = 0
    totalvisited = 0   
 
    for i in range(frequency):
        sentences = []
        currentNode = nodes[counter]
        counter = counter + 1      
        try:
            for j in range(length):
                if currentNode not in visited:
                    visited.append(currentNode)
                totalvisited = totalvisited + 1    
                path = getPath(currentNode,graph)
                sentences.extend(path)
                currentNode = children[currentNode][random.randint(0,len(children[currentNode])-1)]
        except:
            pass        
        result.append(sentences)     
    
    return result        



def generateWalks():


    paths = list()
    with open("SIGL/DatasetGeneration/dataset.json") as line:
        dataset = json.load(line)


    for graph in dataset:
        paths.append(randomWalk(15,len(list(graph["hash"].keys())),graph))
            
    with open("SIGL/NodeEmbeddings/Dataset.txt", "w") as f:
        for i in paths:
            for s in i:
                f.write(" ".join(s))
                f.write('\n')
    
   

         
