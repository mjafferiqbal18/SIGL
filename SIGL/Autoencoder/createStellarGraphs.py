import json
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import stellargraph as sg

def splitComponents(pathName):
        componentList = pathName.split("/")
        componentList.pop(0)
        if '' in componentList:
            componentList.remove('')
        return componentList

def convertToStellar(graph, validation = False, alacarte = None):

    src = []
    dest = []

    for edge in graph["edges"]:
        src.append(edge[1])
        dest.append(edge[0])

    final_edges = {"source": src, 'target': dest}

    square_edges = pd.DataFrame(final_edges)

    wv = KeyedVectors.load("SIGL/NodeEmbeddings/word2vec.wordvectors", mmap='r')

    embeddingmatrix = []

    def getSum():

        for i in graph["hash"].values():
            components = splitComponents(i)
            normalized_matrix = []
            normalized_matrix = word2vec(components)            
            embeddingmatrix.append(normalized_matrix)

    def word2vec(components):
        summed_matrix = np.zeros(128)   
        for component in components:
            if validation == True and component in alacarte:
                summed_matrix = summed_matrix + alacarte[component]
            else:
                summed_matrix = summed_matrix  + wv[component]
        normalized_matrix = summed_matrix / len(components)
        return normalized_matrix    

        
    getSum()

    embed = pd.DataFrame(embeddingmatrix, index = graph["hash"].keys())

    G = sg.StellarGraph(embed, square_edges.astype(str))

    return G






def getGraphs():

    stellarGraphs = []

    with open("SIGL/DatasetGeneration/dataset.json") as line:
        graphs = json.load(line)

    for graph in graphs:
        G = convertToStellar(graph)        
        stellarGraphs.append(G)

    return stellarGraphs



