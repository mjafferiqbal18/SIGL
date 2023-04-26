import json
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import stellargraph as sg

stellarGraphs = []

def getGraphs():
    
    with open("../DatasetGeneration/dataset.json") as line:
        graphs = json.load(line)


    for graph in graphs:

        src = []
        dest = []

        for edge in graph["edges"]:
            src.append(edge[1])
            dest.append(edge[0])

        final_edges = {"source": src, 'target': dest}
        square_edges = pd.DataFrame(final_edges)

        #print(square_edges)

        def splitComponents(pathName):
            componentList = pathName.split("/")
            componentList.pop(0)
            return componentList

        wv = KeyedVectors.load("../NodeEmbeddings/word2vec.wordvectors", mmap='r')

        embeddingmatrix = []

        def getSum():
            for i in graph["hash"].values():
                components = splitComponents(i)
                summed_matrix = np.zeros(128)
                for component in components:
                    summed_matrix = summed_matrix  + wv[component]
                normalized_matrix = summed_matrix / len(components)
                embeddingmatrix.append(normalized_matrix)

        getSum()

        embed = pd.DataFrame(embeddingmatrix, index = graph["hash"].keys())

        G = sg.StellarGraph(embed, square_edges.astype(str))

        stellarGraphs.append(G)

    return stellarGraphs