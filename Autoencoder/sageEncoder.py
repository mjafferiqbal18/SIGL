import numpy as np
import pandas as pd
import json
from tensorflow import keras
from keras import layers, optimizers, losses, metrics, Model, models
from stellargraph.mapper import GraphSAGENodeGenerator
from stellargraph.layer import GraphSAGE
from createStellarGraphs import getGraphs
from stellargraph.mapper import FullBatchNodeGenerator
from stellargraph.layer import GCN
import stellargraph as sg

graphs = getGraphs()

print(graphs)

batch_size = 32
num_samples = [10, 5]

generator = sg.mapper.PaddedGraphGenerator(graphs)
gc_model = sg.layer.GCNSupervisedGraphClassification(
    [64, 32], ["relu", "relu"], generator, pool_all_layers=True
)

x_inp, x_out = gc_model.in_out_tensors()

decoder = layers.Dense(128, activation="linear")(x_out)

model = Model(inputs=x_inp, outputs=decoder)
model.compile(
    optimizer=optimizers.Adam(learning_rate=0.01),
    loss=losses.MeanSquaredError(),
    metrics=[metrics.MeanAbsoluteError()],
)

autoencoder = Model(inputs=x_inp, outputs=model(x_inp))

num_epochs = 200

# Get the node features as target data
target_data = graphs.node_features()

# Create a generator flow with the target data
batch = generator.flow(graphs.nodes(), target_data)

history = model.fit(batch, epochs=num_epochs, verbose=1)



# # Create a GraphSAGE-based encoder
# def create_graphsage_encoder(graph, layer_sizes=[64, 32]):
#     generator = GraphSAGENodeGenerator(graph, batch_size=len(graph.nodes()), num_samples=[10, 5])
#     graphsage = GraphSAGE(layer_sizes=layer_sizes, generator=generator, bias=True, dropout=0.5)
#     x_inp, x_out = graphsage.in_out_tensors()
#     return Model(inputs=x_inp, outputs=x_out[0]), generator

# # Train a GraphSAGE-based encoder and MLP decoder on all graphs
# embedding_size = 128

# # Create the GraphSAGE encoder model
# first_graph = graphs[0]
# encoder, _ = create_graphsage_encoder(first_graph)

# # Create the MLP decoder model
# inputs = layers.Input(shape=(embedding_size,))
# decoder = layers.Dense(64, activation="relu")(inputs)
# decoder = layers.Dense(embedding_size, activation="linear")(decoder)
# decoder = Model(inputs=inputs, outputs=decoder)

# # Combine the GraphSAGE encoder and MLP decoder into a single autoencoder model
# x_inp, x_out = encoder.input, decoder(encoder.output)
# autoencoder = Model(inputs=x_inp, outputs=x_out)

# # Train the autoencoder on each graph one by one
# autoencoder.compile(optimizer=optimizers.Adam(lr=1e-3), loss=losses.MeanSquaredError())
# for graph in graphs:
#     generator = GraphSAGENodeGenerator(graph, batch_size=len(graph.nodes()), num_samples=[10, 5])
#     node_ids = graph.nodes()
#     history = autoencoder.fit(generator.flow(node_ids, node_ids), epochs=100, verbose=1)

