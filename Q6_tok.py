#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 18:18:05 2020

@author: VictorRosi
"""


# coding: utf-8

import json
import pathlib
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import FrenchStemmer


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


with open("./corpus_rearranged_1/Q6_affect.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
        
# load stop words in a file
stopWord_path = '/Users/VictorRosi/Documents/GitHub/interview_analysis/'
file = "new_stopwords_fr.txt"
stopFile = open(stopWord_path+file, 'r', encoding="utf-8")
yourResult = np.array([line.split('\n')
                       for line in stopFile.readlines()])[:, 0]
stopWord = list(yourResult)


lemm_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/lemm_file.json'
# Open lemm file
with open(lemm_file, encoding="utf-8") as json_file:
        lemms = json.load(json_file)


        
term = 'chaud'
term_list = []
op_term_list = []
index_ID = []
word_list = []
unDup = {}


tokenizer = nltk.RegexpTokenizer(r'\w+')

for index, dic in enumerate(data[term]):
    term_list.append(dic["term"])
    op_term_list.append(dic["not"])
    index_ID.append(dic["expertID"])
    
for index, answer in enumerate(term_list):
    tokenized = []
    tokenized = tokenizer.tokenize(answer.lower())
    print(len(tokenized))
    tokenized = list(dict.fromkeys(tokenized))
    print(len(tokenized))
    for j, word in enumerate(tokenized):
        if word not in stopWord:
            res = lemmatization(word, lemms)
            if res == '':
                    #print(word)
                    res = word
            word_list.append(res)
            
# sort and count
for index, word in enumerate(set(word_list)):
    unDup[word] = word_list.count(word)
    # sort from most to least used
word_list = sorted(unDup.items(), key=lambda t: t[1], reverse=True)
