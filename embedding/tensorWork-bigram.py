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
outputdir = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/output'
corpus_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/corpus/brillant.json'
embedding_file = 'frWac_no_postag_no_phrase_700_skip_cut50.bin'

for root, dirs, files in os.walk(outputdir):
    for file in files:
        os.remove(os.path.join(root, file))
        


#%%

with open(path + 'rond_Q2Q5_2.json') as json_file:
    data = json.load(json_file)
    
bigram_data = [x for x in data]
bigram_data_freq = [data[x] for x in data]


#%%

model = KeyedVectors.load_word2vec_format(embedding_file, binary=True, encoding='utf-8')
words_emb = model.index2word
embeddings = [model[x] for x in words_emb]

# init writer for tensorboard
writer = SummaryWriter(outputdir)

#%%



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
        
#%%
        

writer.add_embedding(np.array(bigram_emb), metadata=bigram_list)
writer.close()


