from validation import convertGraph,reconstructNodes
import sys
import numpy as np
from keras.models import load_model

def main():

    print("Converting Graph..")
    trainingGraph = sys.argv[1]
    graph = convertGraph(trainingGraph,val=False)

    print("Reconstructing Nodes..")
    autoencoder = load_model("autoencoder.h5")
    loss = reconstructNodes(graph,autoencoder)

    abnormal = False

    with open("threshold.txt", "r") as f:
        content = f.read()

    threshold = np.float32(content)

    score = np.mean(list(loss.values()))

    if score > threshold:
        abnormal = True

    if abnormal == True:

        process = {}
        _,Dict = graph
        print("Malicious Nodes Detected") 

        for id,val in loss.items():
            process[Dict["hash"][id]] = val

        sortedProcesses = dict(sorted(process.items(), key=lambda x: x[1], reverse=True))

        for name,val in sortedProcesses.items():
            print("Process:", name, "Reconstruction loss:", val)
    else:
        print("No Malicious Nodes Found")    


main()