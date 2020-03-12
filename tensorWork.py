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

cutoff = 2
path = "corpus_lemm/"
outputdir = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/output'
corpus_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/corpus/brillant.json'
embedding_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/frWiki_no_phrase_no_postag_500_cbow_cut10.bin'


for root, dirs, files in os.walk(outputdir):
    for file in files:
        os.remove(os.path.join(root, file))
        


#%%

with open(path + 'rond_Q2_.json') as json_file:
    data = json.load(json_file)
    
words_data = [x for x in data if data[x]['freq'] >= cutoff]
words_data_freq = [data[x]['freq'] for x in data if data[x]['freq'] >= cutoff]


#%%

model = KeyedVectors.load_word2vec_format(embedding_file, binary=True, encoding='utf-8')
words_emb = model.index2word
embeddings = [model[x] for x in words_emb]

# init writer for tensorboard
writer = SummaryWriter(outputdir)

#%%

# turn to dict
embedding_dict = dict(zip(words_emb, embeddings))
    
    

words_list = []
freq_list = []
for i,word in enumerate(words_data):
    if word in words_emb:
        words_list.append(word)
        freq_list.append(words_data_freq[i])
    # else:
    #     print(word, words_data_freq[i])
        
#%%
        
embed = [embedding_dict[x] for x in words_list]


writer.add_embedding(np.array(embed), metadata=words_list)
writer.close()


