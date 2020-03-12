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

term = 'rugueux'
question = 'Q2'

unigram_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corpus_lemm/json/'+term+'_'+question+'_corr_.json'


# Open unigram/frequency file
with open(unigram_file) as json_file:
    uni_data = json.load(json_file)

data_list = []
for index, word in enumerate(set(uni_data)):
    data_list.append([word, uni_data[word]['freq'], uni_data[word]['words'], uni_data[word]['ID']])
    
data_list.sort(key=lambda t: t[1], reverse=True)

# Generate dataframe from list and write to xlsx.
output_dir = './corpus_lemm/xls/'
pd.DataFrame(data_list).to_excel(output_dir+term+'_'+question+'_.xlsx', header=False, index=False)

        
        
