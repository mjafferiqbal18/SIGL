import subprocess
from gensim.models import KeyedVectors
from SIGL.NodeEmbeddings.randomWalks import randomWalk
import os
import time

def alacarte(targets,graph):

    dictionary = {}
    carte = {}

    wv = KeyedVectors.load("SIGL/NodeEmbeddings/word2vec.wordvectors", mmap='r')

    path = randomWalk(15,len(list(graph["hash"].keys())),graph)

    with open("SIGL/NodeEmbeddings/carte/Dataset.txt", "w") as f:
        
        for s in path:
            f.write(" ".join(s))
            f.write('\n')

    for word in wv.key_to_index:
        dictionary[word] = wv[word]


    with open('SIGL/NodeEmbeddings/carte/source.txt', 'w') as file:
        for key, value in dictionary.items():
            file.write(key + ' ' + ' '.join(str(v) for v in value) + '\n')

    with open('SIGL/NodeEmbeddings/carte/targets.txt', 'w') as file:
        for target in targets:
            file.writelines(target + '\n')

    

    command = ["python", "SIGL/NodeEmbeddings/carte/alacarte.py", "output", "-s", "SIGL/NodeEmbeddings/carte/source.txt", "-c", "SIGL/NodeEmbeddings/carte/Dataset.txt", "-w", "5"]
    subprocess.run(command)

    command2 = ["python", "SIGL/NodeEmbeddings/carte/alacarte.py", "output", "-s", "SIGL/NodeEmbeddings/carte/source.txt", "-c", "SIGL/NodeEmbeddings/carte/Dataset.txt", "-w", "5", "-t" , "SIGL/NodeEmbeddings/carte/targets.txt"]
    subprocess.run(command2)


    
    with open("output_alacarte.txt", 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, *values = line.split()
                carte[key] = [float(value) for value in values]
        
    files = ["output_alacarte.txt", "output_not_found.txt", "output_source_context_vectors.bin", "output_target_context_vectors.bin", "output_source_vocab_counts.txt", "output_target_vocab_counts.txt", "output_transform.bin"]
    
    for file in files:
        if os.path.isfile(file): 
            os.remove(file)
 
    return carte


