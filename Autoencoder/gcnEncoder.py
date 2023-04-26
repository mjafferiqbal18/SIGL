import json
import random
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import stellargraph as sg
from stellargraph.mapper import FullBatchNodeGenerator
from stellargraph.layer import GCN
from tensorflow import keras

from keras import layers, optimizers, losses, metrics, Model, models
from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Activation

with open("onedrive.json") as line:
    graph = json.load(line)

edges = list()
src = []
dest = []

def generatePairs():
    pair = dict()
    for i in graph:
        if "id" in i:
            if i['type'] == "Artifact":
                pair[i['id']] = i['annotations']['path']
            if i['type'] == "Process":
                pair[i['id']] = i['annotations']['exe']
        else:
            src.append(i['to'])
            dest.append(i['from'])
            edges.append((i['to'],i['from']))
    return pair


nodes = generatePairs()
node_paths = list(nodes.values())





# def createMatrix():
#     num_nodes = len(nodes.keys())
#     print(num_nodes, type(num_nodes))
#     Admatrix = np.zeros((num_nodes,num_nodes))
#     hashes = list(nodes.keys())
#     for i in edges:
#         Admatrix[hashes.index(i[0])][hashes.index(i[1])] = 1
#     return Admatrix

# adjancenyMatrix = createMatrix()



final_edges = {"source": src, 'target': dest}



square_edges = pd.DataFrame(final_edges)

#print(square_edges)

def splitComponents(pathName):
    componentList = pathName.split("/")
    componentList.pop(0)
    return componentList


# print(getSum('/usr/bin/python'))\

#print(node_paths)

wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')


#print(wv['usr'])

embeddingmatrix = []

def getSum(path):
    final = []
    for i in node_paths:
        components = splitComponents(i)
        embeddingmatrix.append(wv[components[0]])
getSum("")

print(len(embeddingmatrix), len(embeddingmatrix[0]))

embed = pd.DataFrame(embeddingmatrix, index = nodes.keys())


G = sg.StellarGraph(embed, square_edges.astype(str))

generator = FullBatchNodeGenerator(G, method="gcn")

gcn = GCN(
    layer_sizes=[64,32], activations=["relu","relu"], generator=generator, dropout=0.5
)

x_inp, x_out = gcn.in_out_tensors()

# embedding_model = Model(inputs=x_inp, outputs=x_out)

# all_gen = generator.flow(embed.index)

# emb = embedding_model.predict(all_gen)

# emb = emb[0]
# print(emb.shape)

decoder = layers.Dense(128, activation="linear")(x_out)

# Create the Keras model
model = Model(inputs=x_inp, outputs=decoder)
model.compile(
    optimizer=optimizers.Adam(learning_rate=0.01),
    loss=losses.MeanSquaredError(),
    metrics=[metrics.MeanAbsoluteError()],
)

autoencoder = Model(inputs=x_inp, outputs=model(x_inp))

num_epochs = 200

# Get the node features as target data
target_data = G.node_features()

# Create a generator flow with the target data
batch = generator.flow(G.nodes(), target_data)

history = model.fit(batch, epochs=num_epochs, verbose=1)


#print(history)
# # Create a generator flow for the graph
flow = generator.flow(G.nodes())

# Get the original node features
original_features = G.node_features()

# Get the reconstructed node features
reconstructed_features = autoencoder.predict(flow)[0]

# # Calculate the mean squared error between the original and reconstructed features
mse = losses.MeanSquaredError()(original_features, reconstructed_features).numpy()


print(mse)