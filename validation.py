import os
import numpy as np
from tensorflow import keras
from SIGL.DatasetGeneration.generateTrainingData import processSPADEJSON
from keras.models import load_model
from SIGL.Autoencoder.createStellarGraphs import convertToStellar, splitComponents
from gensim.models import KeyedVectors
from SIGL.NodeEmbeddings.ALaCarte.gen import alacarte
from jenkspy import JenksNaturalBreaks
import sys


def convertGraph(graph, val = True):

    graphName = graph.split("-")[0]

    directory = ""

    if val == True:
        print(graph)
        directory = "validationGraphs"
    else:
        directory = "testingGraphs"

    if graphName == "skype":
        testDict = processSPADEJSON(graph,f"./{directory}/{graph}","/usr/bin/skypeforlinux")
    elif graphName == "teamviewer":
        testDict = processSPADEJSON(graph,f"./{directory}/{graph}","/usr/bin/teamviewer")
    
    targets = []

    wv = KeyedVectors.load("SIGL/NodeEmbeddings/word2vec.wordvectors", mmap='r')

    for i in testDict["hash"].values():
        for j in splitComponents(i):
            if j not in wv.key_to_index:
                if j not in targets and j != '':
                    targets.append(j)

    unseen = {}

    if len(targets) > 0:
        unseen = alacarte(targets, testDict)

    Graph = convertToStellar(testDict, validation = True, alacarte=unseen)

    return (Graph,testDict)



def JenksMaxZoneAvg(nodeLosses):
    x = JenksNaturalBreaks(3)
    x.fit(nodeLosses)
    return max(np.mean(x.groups_[0]),np.mean(x.groups_[1]),np.mean(x.groups_[2]))


def reconstructNodes(graph,autoencoder):

    Graph,Dict = graph
    processNodes = []

    for i in Dict["types"].keys():
        if Dict["types"][i] == 1:
            processNodes.append(i)

    orignalFeatures = Graph.node_features(nodes = processNodes)
    newFeatures = autoencoder.predict(orignalFeatures)        

    loss = {}

    counter = 0
    for i in processNodes:
        mse = np.mean(np.power(newFeatures[counter] - orignalFeatures[counter], 2))
        loss[i] = mse
        counter = counter + 1

    return loss





def main():

    print("Obtaining Graphs..")

    validationGraphs = os.listdir("./validationGraphs")

    graphs = []

    for graph in validationGraphs:

        graphs.append(convertGraph(graph))


    print("Reconstructing Nodes..")

    autoencoder = load_model("autoencoder.h5")

    thresholdList = []

    for i in graphs:

        largestAverageLoss = JenksMaxZoneAvg(list(reconstructNodes(i,autoencoder).values()))
        thresholdList.append(largestAverageLoss)

    print("Setting Threshold..")

    std = np.std(thresholdList)
    mean = np.mean(thresholdList)
    threshold =  mean + 3 * std

    with open("threshold.txt", "w") as f:
        f.write(str(threshold))

    print("Done")



if sys.argv[0] == "validation.py":
    main()