from gensim.models import Word2Vec


def source(word_vectors):
    
    src = []
    
    for i in word_vectors.index_to_key:
      src.append({i:word_vectors.get_vector(i)})

    with open("SIGL/NodeEmbeddings/ALaCarte/source.txt", "w") as f:
      for i in src:
          for key,value in i.items():
            f.write(key + ' ' + ' '.join(str(v) for v in value) + '\n')



def embeddings():
    
    data = []

    with open("SIGL/NodeEmbeddings/Dataset.txt", "r") as f:
      for line in f:
        data.append(line.split())


    embedder = Word2Vec(window=5, sg=1, hs=0, min_count=1, vector_size = 128, shrink_windows=True
    )

    # Build Vocabularys
    embedder.build_vocab(data)


    # Train
    embedder.train(
      data, total_examples=embedder.corpus_count, epochs=20
    )

    word_vectors = embedder.wv

    source(word_vectors)

    word_vectors.save("SIGL/NodeEmbeddings/word2vec.wordvectors")




