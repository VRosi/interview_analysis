#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:41:09 2020

@author: VictorRosi
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:54:46 2020

@author: VictorRosi
"""

import torch
from torch.utils.tensorboard import SummaryWriter
from gensim.models.keyedvectors import KeyedVectors
import json
import re
import os, os.path
import nltk
import numpy as np
from embedding_func import embedding_token_gen, embedding_visualization


term = 'brillant'
question = 'Q2'
cutoff = 2

corpus_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corpus_rearranged_1/'+term+'.json'
expert_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/expert_index.json'
unigram_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corpus_lemm/'+term+'_'+question+'_.json'


#%% Load files
# Open corpus file
with open(corpus_file) as json_file:
    data = json.load(json_file)
    
        
# Open expert file
with open(expert_file) as json_file:
    ex_data = json.load(json_file)
    
# Open unigram/frequency file
with open(unigram_file) as json_file:
    uni_data = json.load(json_file)
    
# Open stop word file for embedding only
file = "/Users/VictorRosi/Documents/GitHub/interview_analysis/new_stopwords_fr.txt"
stopFile = open(file, 'r', encoding="utf-8")
yourResult = np.array([line.split('\n')
                       for line in stopFile.readlines()])[:, 0]
stopWord = list(yourResult)
file = "/Users/VictorRosi/Documents/GitHub/interview_analysis/minus_stopwords.txt"
stopFile = open(file, 'r', encoding="utf-8")
temp = [line.split(' ') for line in stopFile.readlines()]
exStopWord = temp[0]
# qq
# Open lemm file for embedding only
lemm_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/lemm_file.json'
with open(lemm_file, encoding="utf-8") as json_file:
        lemms = json.load(json_file)
        

answers = []
ID = []
prof = []

for i, k in enumerate(data[question]):
    answers.append(k['answer'])
    ID.append(k['expertID'])
    
#%% QUERY WORDS
query_lemm = ['aigu']
query_word = []
for index, lemm in enumerate(set(uni_data)):
    if uni_data[lemm]['freq'] >= cutoff and lemm in query_lemm:
        query_word += uni_data[lemm]['words']
        
#%% INDEX SENTENCES IN CORPUS

sentences_list = []
sentence_query = {}

for i,answer in enumerate(answers):
    sentences = []
    sent_temp  =[]
    sentences = re.split(r'[\.*,*?]| et ', answer)
    for j, sentence in enumerate(sentences):
        for word in query_word:
            if word in sentence:
                sent_temp.append(sentence)
    sentence_query[ID[i]] = sent_temp
    
for i, query in enumerate(set(sentence_query)):
    sentence_query[query] = list(dict.fromkeys(sentence_query[query]))


    