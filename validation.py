import os
import numpy as np
from tensorflow import keras
from SIGL.DatasetGeneration.generateTrainingData import processSPADEJSON
from keras.models import load_model
from SIGL.Autoencoder.createSpekralGraphs import converttoSpektral, splitComponents
from gensim.models import KeyedVectors
from SIGL.NodeEmbeddings.carte.gen import alacarte
from jenkspy import JenksNaturalBreaks
import sys
from SIGL.Autoencoder.autoencoder import autoencoder

def convertGraph(graph, val = True):

    graphName = graph.split("-")[0]

    directory = ""

    if val == True:
        print(graph)
        directory = "SIGL/DatasetGeneration/validationGraphs"
    else:
        directory = "SIGL/DatasetGeneration/testingGraphs"

    execmap = {"7zip":"/usr/bin/p7zip", "onedrive":"/usr/bin/onedrive", "skype": "usr/bin/skypeforlinux", "teamviewer":"usr/bin/teamviewer","winrar":"usr/bin/rar","filezilla":"usr/bin/filezilla","shotcut":"/usr/lib/shotcut","pwsafe":"/usr/bin/pwsafe","firefox":"/usr/bin/firefox","dropbox":"/usr/bin/dropbox"}    

    testDict = processSPADEJSON(graph,f"./{directory}/{graph}",execmap[graphName])

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

    Graph = converttoSpektral(testDict, validation = True, alacarte=unseen)

    return (Graph,testDict)



def JenksMaxZoneAvg(nodeLosses):
    x = JenksNaturalBreaks(3)
    x.fit(nodeLosses)
    return max(np.mean(x.groups_[0]),np.mean(x.groups_[1]),np.mean(x.groups_[2]))


def reconstructNodes(graph,auto):

    Graph,Dict = graph
    processNodes = []

    for index,i in enumerate(Dict["types"].keys()):
        if Dict["types"][i] == 1:
            processNodes.append((index,i))

    emb,adj =  Graph
    orignalFeatures = emb
    newFeatures = auto([emb,adj])     

    loss = {}

    for index,i in processNodes:
        mse = np.mean(np.power(newFeatures[index] - orignalFeatures[index], 2))
        loss[i] = mse

    return loss





def main():

    print("Obtaining Graphs..")

    validationGraphs = os.listdir("SIGL/DatasetGeneration/validationGraphs")

    graphs = []

    for graph in validationGraphs:

        graphs.append(convertGraph(graph))


    print("Reconstructing Nodes..")

    auto = load_model("auto")

    thresholdList = []

    for i in graphs:

        largestAverageLoss = JenksMaxZoneAvg(list(reconstructNodes(i,auto).values()))
        thresholdList.append(largestAverageLoss)

    print("Setting Threshold..")

    std = np.std(thresholdList)
    mean = np.mean(thresholdList)
    threshold =  mean + (3 * std)

    with open("threshold.txt", "w") as f:
        f.write(str(threshold))

    print("Done")


if len(sys.argv) == 1:
    main()