#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:00:11 2020

@author: VictorRosi
"""

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

#%%

with open(path + 'rugueux_Q2_1.json') as json_file:
    data = json.load(json_file)
    
words_data = [x for x in data]
words_data_freq = [data[x] for x in data]


#%%

for root, dirs, files in os.walk(outputdir):
    for file in files:
        os.remove(os.path.join(root, file))

words_emb, embeddings = pickle.load(open('/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/polyglot-fr.pkl', "rb"), encoding='latin1')

# init writer for tensorboard
writer = SummaryWriter(outputdir)

#%%

# turn to dict
embedding_dict = {}
for i, emb in enumerate(embeddings):
    embedding_dict[words_emb[i]] = emb
    
    
words_list = []
freq_list = []
for i,word in enumerate(words_data):
    if word in words_emb:
        words_list.append(word)
        freq_list.append(words_data_freq[i])
    else:
        print(word, words_data_freq[i])
        
#%%
        
embed = [embedding_dict[x] for x in words_list]


writer.add_embedding(np.array(embed), metadata=words_list)
writer.close()




    