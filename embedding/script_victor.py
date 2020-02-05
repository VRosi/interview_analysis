#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:05:41 2020

@author: prang
"""

import torch
from torch.utils.tensorboard import SummaryWriter
import pickle
import numpy as np
import json
import re
import os, os.path



#%%
outputdir = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/output'
corpus_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/corpus/brillant.json'

for root, dirs, files in os.walk(outputdir):
    for file in files:
        os.remove(os.path.join(root, file))

words, embeddings = pickle.load(open('/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/polyglot-fr.pkl', "rb"), encoding='latin1')

# turn to dict
embedding_dict = {}
for i, emb in enumerate(embeddings):
    embedding_dict[words[i]] = emb

# Open corpus
with open(corpus_file) as json_file:
    data = json.load(json_file)

phrases = []
 

for i, k in enumerate(data['Q2']):
    phrases.append(k['answer'])
    
# init writer for tensorboard
writer = SummaryWriter(outputdir)

meta = []
wrd_list = []
for i,phr in enumerate(phrases):
    wrd_list_tmp = []
    wrd_list_tmp2 = []
    wrd_list_tmp = re.split(r'\s*[\.*,\s]\s*', phr)
    for j,w in enumerate(wrd_list_tmp):
        if w in words:
            wrd_list_tmp2.append(w)
            
    wrd_list = wrd_list + wrd_list_tmp2
    meta = meta + [i]*len(wrd_list_tmp2)

"""    
for i,k in enumerate(wrd_list):
    if k=='':
        del wrd_list[i]
        del meta[i]
 """


embed = [embedding_dict[x] for x in wrd_list]
new = [wrd_list, meta]


#writer.add_embedding(embeddings[:100], metadata=words[:100])
writer.add_embedding(np.array(embed), metadata=wrd_list)
writer.close()
# Pour lancer tensorbard
# Dans un terminal
## tensorboard --logdir='path_to_outputdir'