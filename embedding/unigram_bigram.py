#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 17:34:36 2020

@author: VictorRosi
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:01:07 2020

@author: VictorRosi
"""


from gensim.models.keyedvectors import KeyedVectors
import torch
from torch.utils.tensorboard import SummaryWriter
import pickle
import numpy as np
import json
import re
import os, os.path


path = "corpus_lemm/"
embedding_file = 'frWiki_no_phrase_no_postag_500_cbow_cut10.bin'

#%% INITIALIZATION

term = "brillant"
question = "Q2Q5"


#%% EMBEDDING ENHANCE

model = KeyedVectors.load_word2vec_format(embedding_file, binary=True, encoding='utf-8')
words_emb = model.index2word
embeddings = [model[x] for x in words_emb]

#%% UNIGRAM

with open(path + term +'_'+ question +'_1.json') as json_file:
    data = json.load(json_file)
    
words_data = [x for x in data]
words_data_freq = [data[x] for x in data]

# turn to dict
embedding_dict = dict(zip(words_emb, embeddings))
unigram_list = []
freq_list = []
for i,word in enumerate(words_data):
    if word in words_emb:
        unigram_list.append(word)
        freq_list.append(words_data_freq[i])
    else:
        print(word, words_data_freq[i])
        
unigram_emb = [embedding_dict[x] for x in unigram_list]

#%% BIGRAM

with open(path + term +'_'+ question +'_2.json') as json_file:
    data = json.load(json_file)
    
bigram_data = [x for x in data]
bigram_data_freq = [data[x] for x in data]

# turn to dict
embedding_dict = dict(zip(words_emb, embeddings))
bigram_emb = []
bigram_list = []
freq_list = []
for i,bigram in enumerate(bigram_data):
    bigram_vec = bigram.split(' ')
    if bigram_vec[0] in words_emb and bigram_vec[1] in words_emb:
        emb_tmp = []
        emb_tmp = [model[word] for word in bigram_vec]
        bigram_emb.append(sum(emb_tmp))
        bigram_list.append(bigram)
        freq_list.append(bigram_data_freq[i])

    else:
        print(bigram, bigram_data_freq[i])


#%% INIT TENSORBOARD
        
outputdir = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/output'
for root, dirs, files in os.walk(outputdir):
    for file in files:
        os.remove(os.path.join(root, file))
# init writer for tensorboard
writer = SummaryWriter(outputdir)

#%% ENDGAME

total_emb = unigram_emb+bigram_emb
total_list = unigram_list+bigram_list

writer.add_embedding(np.array(total_emb), metadata=total_list)
writer.close()



        
