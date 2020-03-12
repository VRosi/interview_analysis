#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script allows to generate JSON files containing lemmatization, frequency of words in corpus considering : 
    - the studied term
    - the studied question
It also allows to plot the most frequent words considering a cutoff frequency of words.    
"""


import json
import pathlib
import numpy as np
import pandas as pd
import nltk
import re
import csv
import matplotlib.pyplot as plt
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

def n_gram(list, n):
    """
    This function use the zip function to help us generate n-grams
    Concatentate the tokens into ngrams and return
    OUTPUT : - n-gram string
    """
    ngrams = zip(*[list[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def plot_wordF(plot_list, cutoff):
    plot_list = [word for word in word_list if word[1] >= cutoff]
    indexes, values = list(zip(*plot_list))
    bar_width = 0.35
    plt.barh(indexes, values)
    plt.gca().invert_yaxis()
    plt.show()
     

#%% INIT
    
term = "rugueux"
question = "Q2"
# cutoff for plot
cutoff = 2


with open("./corpus_rearranged_1/"+ term +".json", encoding="utf-8") as json_file:
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
        

#%% TOKENIZE
        
word_list = []
unDup = {}
answers = []
lemm_dic = {}
index_ID = []
tokenizer = nltk.RegexpTokenizer(r'\w+')

for i, k in enumerate(data[question]):
    answers.append(k['answer'])
    index_ID.append(k['expertID'])
    
    
for index, answer in enumerate(answers):
    tokenized = []
    # kill duplicates
    tokenized = tokenizer.tokenize(answer.lower())
    tokenized = list(dict.fromkeys(tokenized))
    for j, word in enumerate(tokenized):     
        if word not in stopWord:
            res = lemmatization(word, lemms) 
            if res == '':                              
                res = word
            if res not in stopWord:
                if res in lemm_dic:                
                    lemm_dic[res].append([index_ID[index], word])
                else:
                    lemm_dic[res] = [[index_ID[index], word]]
                    
#%%
# Only to count number of people using a word related to a lemm
# for i, lemm in enumerate(set(lemm_dic)):
#     tmp = []
#     for j, word in enumerate(lemm_dic[lemm]):
#         tmp.append(word[0])
#     tmp = list(dict.fromkeys(tmp))
#     print(lemm, tmp, lemm_dic[lemm])
                    

                
#%% CREATE DICTIONNARY 
new_dic = {}
for i, lemm in enumerate(set(lemm_dic)):
    # Only to count number of people using a word related to a lemm
    tmp_freq = []
    tmp_word = []
    tmp_ID = []
    for j, word in enumerate(lemm_dic[lemm]):
        tmp_freq.append(word[0])
        tmp_word.append(word[1])
    tmp_freq = list(dict.fromkeys(tmp_freq))
    tmp_word = list(dict.fromkeys(tmp_word))
    new_dic[lemm] = {'freq' : len(tmp_freq), 'words' : tmp_word, 'ID' : tmp_freq}
   
        
#%%  SORT & PLOT  
# cutoff frequency of words      
# plot_dic = {}
# for index, lemm in enumerate(set(new_dic)):
#     plot_dic[lemm] = new_dic[lemm]['freq']
# # sort from most to least used
# word_list = sorted(plot_dic.items(), key=lambda t: t[1], reverse=True)

# plot_wordF(word_list, 3) 



#%% GENERATE JSON FILE WITH ARCHITCTURE : 

"""
{'lemm':{
    'freq' : '',
    'words' : '',
    'ID' : '',
    },
    {...}
}

"""
path_j = './corpus_lemm/json/'
#result_dict = dict(zip(lol_word, lol_freq))
jsonfile = json.dumps(new_dic, indent=2)
with open(path_j +term + "_"+question+"_.json", 'w') as f_output:
    f_output.write(jsonfile)
    
# for index, answer in enumerate(answers):
#     tokenized = []
#     # kill duplicates
#     tokenized = tokenizer.tokenize(answer.lower())
#     tokenized = list(dict.fromkeys(tokenized))
#     for j, word in enumerate(tokenized):
#         if word not in stopWord:
#             res = lemmatization(word, lemms)
#             if res == '':
#                     #print(word)
#                     res = word
#             if res not in stopWord:
#                 word_list.append(res)
#                 if res in lemm_dic and word not in lemm_dic[res]:
#                     lemm_dic[res].append(word)
#                 else:
#                     lemm_dic[res] = [word]