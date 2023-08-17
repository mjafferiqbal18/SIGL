from validation import convertGraph,reconstructNodes
import sys
import numpy as np
from keras.models import load_model
from SIGL.Autoencoder.autoencoder import autoencoder
from keras.optimizers import Adam
from keras.losses import MeanSquaredError

def main():

    print("Converting Graph..")
    trainingGraph = sys.argv[1]
    graph = convertGraph(trainingGraph,val=False)

    print("Reconstructing Nodes..")
    auto = load_model("auto")
    los = MeanSquaredError()
    opt = Adam(learning_rate=0.001)
    auto.compile(optimizer=opt, loss=los)
    loss = reconstructNodes(graph,auto)

    abnormal = False

    with open("threshold.txt", "r") as f:
        content = f.read()

    threshold = np.float32(content)

    score = np.mean(list(loss.values()))

    if score > threshold:
        abnormal = True

    print("Anomaly Score:", score, "Threshold:", threshold)

    if abnormal == True:

        process = {}
        _,Dict = graph
        print("Malicious Nodes Detected") 

        for id,val in loss.items():
            process[Dict["hash"][id]] = val

        sortedProcesses = dict(sorted(loss.items(), key=lambda x: x[1], reverse=True))

        for name,val in sortedProcesses.items():
            print("Process:", name, "Name", Dict["hash"][name], "Reconstruction loss:", val)
    else:
        print("No Malicious Nodes Found")    


main()