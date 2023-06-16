import os
import stellargraph as sg
import numpy as np
from tensorflow import keras
from SIGL.DatasetGeneration.generateTrainingData import processSPADEJSON
from keras.models import load_model
from SIGL.Autoencoder.createStellarGraphs import convertToStellar, splitComponents
from gensim.models import KeyedVectors
from SIGL.NodeEmbeddings.ALaCarte.gen import alacarte


graphs = []

validationGraphs = os.listdir("./validationGraphs")


for graph in validationGraphs:

    graphName = graph.split("-")[0]

    if graphName == "skype":
        testDict = processSPADEJSON(f"./validationGraphs/{graph}","/usr/bin/skypeforlinux")
    elif graphName == "teamviewer":
        testDict = processSPADEJSON(f"./validationGraphs/{graph}","/usr/bin/teamviewer")
    
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

    graphs.append((Graph,testDict))


autoencoder = load_model("myModel.h5")

losses = []


for Graph,Dict in graphs:

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


    losses.append(loss) 



  