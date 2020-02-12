#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:23:01 2020

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

corpus_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corpus/rond.json'
lemm_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/lemm_file.json'
expert_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/expert_index.json'
stopWord_path = '/Users/VictorRosi/Documents/GitHub/interview_analysis/'




# Open corpus file
with open(corpus_file) as json_file:
    data = json.load(json_file)
    
    
# Open lemm file
with open(lemm_file, encoding="utf-8") as json_file:
        lemms = json.load(json_file)
        
# Open expert file
with open(expert_file) as json_file:
    ex_data = json.load(json_file)
        
# load stop words in a file
file = "stopwords-fr.txt"
stopFile = open(stopWord_path+file, 'r', encoding="utf-8")
yourResult = np.array([line.split('\n')
                       for line in stopFile.readlines()])[:, 0]
stopWord = list(yourResult)
    
# load exception words in a file
file = "minus_stopwords.txt"
exStopFile = open(stopWord_path+file, 'r', encoding="utf-8")
temp = [line.split(' ') for line in exStopFile.readlines()]
exStopWord = temp[0]

# remove exception words from stopWord list
for word in exStopWord:
    if word in stopWord:
        del stopWord[stopWord.index(word)]

        

answers = []
ID = []
prof = []

for i, k in enumerate(data['Q6']):
    answers.append(k['answer'])
    ID.append(k['expertID'])
    
#%% INIT TENSORBOARD
outputdir = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/output'
for root, dirs, files in os.walk(outputdir):
    for file in files:
        os.remove(os.path.join(root, file))
# init writer for tensorboard
writer = SummaryWriter(outputdir)
    
#%% FUNCTIONS
                
def lemmatization(word, lemms):

    lemmed = ""
    for index, lemm in enumerate(lemms):
        if word in lemms[lemm]:
            lemmed = lemm
            if lemmed == word:
                break

    return lemmed
     
#%%
    
model = KeyedVectors.load_word2vec_format('frWiki_no_phrase_no_postag_500_cbow_cut10.bin', binary=True, encoding='utf-8')
words_emb = model.index2word
embeddings = [model[x] for x in words_emb]
    
    
#%% INDEX

sentences_list = []
sentences_tok_list = []
sentence_ID = []
sentence_prof = []

tokenizer = nltk.RegexpTokenizer(r'\w+')
for i,answer in enumerate(answers):
    sentences = []
    sentences = re.split(r'[\.*,]', answer)
    for j, sentence in enumerate(sentences): 
        # tokenisation
        tokenized = []
        tok_tmp = []
        tokenized = tokenizer.tokenize(sentence.lower())
        # split phrase in 2 if "et" is present, comment if want remove
        if "et" in tokenized:
            new_sentence = " ".join(tokenized[tokenized.index("et")+1:])
            sentences.insert(j+1, new_sentence)
            tokenized = tokenized[:tokenized.index("et")]
        for k,word in enumerate(tokenized):
            # remove stop words
            if word not in stopWord:
                # lemmatize words
                if word != '' and (len(word) > 1 or word == 'à'):
                    wrd_tmp = lemmatization(word,lemms)
                    if wrd_tmp == '':
                        wrd_tmp = word
                    if wrd_tmp in words_emb:
                        tok_tmp.append(wrd_tmp)

        # load a list of tokenized and clean phrases
        if tok_tmp != []:
            sentence_prof.append(ex_data)
            sentence_ID.append(ID[i])
            sentences_list.append(sentence)
            sentences_tok_list.append(tok_tmp)
                    
            
#%% CLEANING
for i, sentence in enumerate(sentences_tok_list):
    if len(sentence) < 2:
        del sentences_tok_list[i]
        del sentences_list[i]
        del sentence_ID[i]
        
#%% Compute embedding vector
sentences_emb = []
            
for i, sentence in enumerate(sentences_tok_list):
    emb_tmp = []
    emb_tmp = [model[word] for word in sentence]
    sentences_emb.append(sum(emb_tmp))


#%%
    
    
embedding_dict = dict(zip(sentences_list, sentences_emb))

writer.add_embedding(np.array(sentences_emb), metadata=sentences_list)
writer.close()


