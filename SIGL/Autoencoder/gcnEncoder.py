import numpy as np
import pandas as pd
import stellargraph as sg
from stellargraph.mapper import FullBatchNodeGenerator
from stellargraph.layer import GCN
from tensorflow import keras
from createStellarGraphs import getGraphs
from keras import layers, optimizers, losses, metrics, Model, models
from keras.layers import Dense, Activation, Dropout, Input

def helper(att):
    print("\n",att)
    print(att.shape,"\n\n")
    print(type(att))

graphs = getGraphs()

input_layer = Input(shape=(128,))

generator = sg.mapper.PaddedGraphGenerator(graphs)

gc_model = sg.layer.GCNSupervisedGraphClassification(
    [128], ["relu"], generator, pool_all_layers=True
)

inp1, out1 = gc_model.in_out_tensors()

embedding_model = keras.Model(inp1, out1)

embeddings = embedding_model.predict(generator.flow(graphs))


input_layer = Input(shape=(128,))

# Define the encoder layers
encoded = Dense(64, activation='relu')(input_layer)
encoded = Dense(32, activation='relu')(encoded)


# Define the decoder layers
decoded = Dense(64, activation='relu')(encoded)
decoded = Dense(128, activation='sigmoid')(decoded)


autoencoder = Model(inputs=input_layer, outputs=decoded)

# Compile the autoencoder model
autoencoder.compile(optimizer='adam', loss='mean_squared_error')


autoencoder.fit(embeddings, embeddings, epochs=100, batch_size=32)




