
%reset
import pickle
import numpy
import word2vec

with open('polyglot-fr.pkl', 'rb') as f:
    words, embeddings = pickle.load(f, encoding='latin1')
    print("Embeddings shape is {}".format(embeddings.shape))
words[120], embeddings[120]

model = word2vec.load('frwiki.skip.size300.win10.neg15.sample1e-5.min15')
