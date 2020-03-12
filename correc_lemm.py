#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:25:54 2020

@author: VictorRosi
"""

import torch
import json
import re
import os, os.path
import nltk
import pandas as pd
import numpy as np

term = 'brillant'
question = 'Q2'


unigram_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corpus_lemm/json/'+term+'_'+question+'_.json'

#%%
def lemmatization(word, lemms):

    lemmed = ""
    for index, lemm in enumerate(lemms):
        if word in lemms[lemm]:
            lemmed = lemm
            if lemmed == word:
                break

    return lemmed



# Open unigram/frequency file
with open(unigram_file) as json_file:
    data = json.load(json_file)

uni_data = {}
for index, word in enumerate(set(data)):
      uni_data[word] = data[word]

#%%    

lemm_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corr_lemm_file.json'
# Open lemm file
with open(lemm_file, encoding="utf-8") as json_file:
        lemms = json.load(json_file)


for j, word in enumerate(set(uni_data)):  
    for i, lemm in enumerate(set(lemms)):
        if word in lemms[lemm]:
            if lemm in uni_data:
                uni_data[lemm]['words'] += uni_data[word]['words']
                uni_data[lemm]['ID'] += uni_data[word]['ID']
                uni_data[lemm]['ID'] = list(dict.fromkeys(uni_data[lemm]['ID']))
                uni_data[lemm]['freq'] = len(uni_data[lemm]['ID'])                                                
                del uni_data[word]
            

path_j = './corpus_lemm/json/'
#result_dict = dict(zip(lol_word, lol_freq))
jsonfile = json.dumps(uni_data, indent=2)
with open(path_j +term + "_"+question+"_corr_.json", 'w') as f_output:
    f_output.write(jsonfile)            
            
            
            
            
            
            