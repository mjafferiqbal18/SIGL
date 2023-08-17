from SIGL.DatasetGeneration.generateTrainingData import generateDataset

print("Processing Dataset..")
generateDataset()

from SIGL.NodeEmbeddings.randomWalks import  generateWalks

print("Performing random walks...")
generateWalks()


from SIGL.NodeEmbeddings.generateEmbeddings import embeddings

print("Generating embeddings...")
embeddings()


from SIGL.Autoencoder.autoencoder import autoencoder

print("Training Autoencoder...")
autoencoder()



print("Model Saved")