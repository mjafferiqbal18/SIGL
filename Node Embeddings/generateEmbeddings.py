from gensim.models import Word2Vec

data = []

with open("Dataset.txt", "r") as f:
  for line in f:
    data.append(line.split())


embedder = Word2Vec(window=5, sg=1, hs=0, min_count=1, vector_size = 128
)

# Build Vocabularys
embedder.build_vocab(data)


# Train
embedder.train(
   data, total_examples=embedder.corpus_count, epochs=20
)

word_vectors = embedder.wv
word_vectors.save("word2vec.wordvectors")

