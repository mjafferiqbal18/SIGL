from SIGL.NodeEmbeddings.randomWalks import  generateWalks

print("Performing random walks...")
generateWalks()
print("Done")


from SIGL.NodeEmbeddings.generateEmbeddings import embeddings

print("Generating embeddings...")
embeddings()
print("Done")


from SIGL.Autoencoder.gcnEncoder import autoencoder

print("Training Autoencoder...")
autoencoder()
print("Done")


print("Saving Model")