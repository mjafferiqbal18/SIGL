import json
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import stellargraph as sg
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import scipy.sparse as sp
from spektral.data import Graph,BatchLoader,Dataset, SingleLoader

def splitComponents(pathName):
        componentList = pathName.split("/")
        componentList.pop(0)
        if '' in componentList:
            componentList.remove('')
        return componentList

def converttoSpektral(graph, validation = False, alacarte = None):

    arr = [[],[]]

    hashmap = {}
    adj = np.zeros([len(graph["hash"].keys()),len(graph["hash"].keys())])
    

    for index,val in enumerate(graph["hash"].keys()):
        hashmap[val] = index

    for edge in graph["edges"]:
        adj[hashmap[edge[1]]][hashmap[edge[0]]] =  1
        adj[hashmap[edge[0]]][hashmap[edge[1]]] =  1

    wv = KeyedVectors.load("SIGL/NodeEmbeddings/word2vec.wordvectors", mmap='r')

    embeddingmatrix = []

    def word2vec(components):
        summed_matrix = np.zeros(128)   
        for component in components:
            if validation == True and component in alacarte:
                summed_matrix = summed_matrix + alacarte[component]
            else:
                summed_matrix = summed_matrix  + wv[component]
        normalized_matrix = summed_matrix /np.linalg.norm(summed_matrix)
        return normalized_matrix    


    def getSum():

        for i in graph["hash"].values():
            components = splitComponents(i)
            normalized_matrix = []
            normalized_matrix = word2vec(components)         
            embeddingmatrix.append(normalized_matrix)

        
    getSum()

    numembed = np.array(embeddingmatrix)


    class MyDataset(Dataset):
            def read(self):
                    return [Graph(x=numembed, a=sp.csr_matrix(adj))]
    dataset = MyDataset()
    gra = Graph(x=numembed, a=sp.csr_matrix(adj))

    loader = SingleLoader(dataset)
    emb, adj = loader.__next__()

    return (emb,adj)


def getGraphs():

    spektralGraphs = []

    with open("SIGL/DatasetGeneration/dataset.json") as line:
        graphs = json.load(line)

    for graph in graphs:
        G = converttoSpektral(graph)        
        spektralGraphs.append(G)

    return spektralGraphs



