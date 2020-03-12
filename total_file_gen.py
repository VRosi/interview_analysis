#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 10:53:07 2020

@author: VictorRosi
"""

import json
import nltk


words = ["brillant","chaud","rond","rugueux"]
Q = ["Q2"]

#%% FUNCTIONS
                
def lemmatization(word, lemms):

    lemmed = ""
    for index, lemm in enumerate(lemms):
        if word in lemms[lemm]:
            lemmed = lemm
            if lemmed == word:
                break

    return lemmed

answer_tot =  []
index_ID = []


for term in words:
    with open("./corpus_rearranged_1/"+ term +".json", encoding="utf-8") as json_file:
        data = json.load(json_file)
    for quest in Q:
        answer_tmp = []
        for i, k in enumerate(data[quest]): 
            answer_tmp.append(k["answer"])
            index_ID.append(k['expertID'])
        answer_tot.append(answer_tmp)

answer_fin = []
new_dic = {}


for i in range(len(answer_tot[0])):
    ans_tmp = ""
    for j, term in enumerate(answer_tot):        
        ans_tmp += answer_tot[j][i]
    answer_fin.append({'expertID' : index_ID[i], 'answer' : ans_tmp})
    
new_dic["Q"] = answer_fin
    
    


path_j = './corpus_rearranged_1/'
#result_dict = dict(zip(lol_word, lol_freq))
jsonfile = json.dumps(new_dic, indent=2)
with open(path_j +"total_Q2.json", 'w') as f_output:
    f_output.write(jsonfile)