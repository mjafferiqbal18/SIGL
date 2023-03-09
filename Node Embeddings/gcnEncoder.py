import json
import random
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
#import stellargraph

with open("onedrive.json") as line:
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
node_paths = list(nodes.values())





def createMatrix():
    num_nodes = len(nodes.keys())
    print(num_nodes, type(num_nodes))
    Admatrix = np.zeros((num_nodes,num_nodes))
    hashes = list(nodes.keys())
    for i in edges:
        Admatrix[hashes.index(i[0])][hashes.index(i[1])] = 1
    return Admatrix

adjancenyMatrix = createMatrix()

print(adjancenyMatrix)


def splitComponents(pathName):
    componentList = pathName.split("/")
    componentList.pop(0)
    return componentList


# print(getSum('/usr/bin/python'))\

print(node_paths)

wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')


#print(wv['usr'])

embeddingmatrix = []

def getSum(path):
    final = []
    for i in node_paths:
        components = splitComponents(i)
        embeddingmatrix.append(wv[components[0]])
getSum("")


print(len(embeddingmatrix[7]))