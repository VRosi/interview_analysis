#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:37:25 2020

@author: VictorRosi


compte proportions

"""

cat_name = ["Sound",'Dyn',"Spec",'Temp','Ex','Source','CMC','Matter','A/B','Affect','Ref']

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import ast

terms = ["brillant",'chaud','rond','rugueux']
tot_types = []
tot_tokens = []
tot_TTR= []
tot_props = []
opt = 0
for term in terms:
    df = pd.read_excel(r"res_cat/"+ term +"_Q2_.xlsx")
    
    categories = dict.fromkeys(df["cat"].tolist())
    types = defaultdict(list)
    tokens = defaultdict(list)
    props = defaultdict(list)
    cat_tmp = defaultdict(list)
    cat_tmp2 = defaultdict(list)
    cat = df["cat"].tolist()
    lemmas = df['lemma'].tolist()
    freq = df['freq'].tolist()
    expert = df['expert'].tolist()
    
    for index, lemm in enumerate(lemmas):
            cat_tmp[cat[index]].append(freq[index])
        
    for index, lemm in enumerate(lemmas):
            cat_tmp2[cat[index]]+=(ast.literal_eval(expert[index]))
    
    for i, keys in enumerate(set(cat_tmp)):
            tokens[keys] = sum(cat_tmp[keys])
            # prop of experts per category
            numerator = len(list(dict.fromkeys(cat_tmp2[keys])))           
            props[keys] = (numerator/32)*100
            
    for category in [ele for ind, ele in enumerate(cat,1) if ele not in cat[ind:]]:
        types[category] = cat.count(category)
        #print(cat.count(category), term, category)
    
    type_list = []
    token_list = []
    ttr_list = []
    prop_list = []
    
    for i, name in enumerate(cat_name):
        if name == "A/B":
            name = "Action/Behavior"
        if name == "Temp":
            name = "Temporal"
        if name == "Ex":
            name = "Excitation"
        if name == "Ref":
            name = "Reference"
        if name == "Dyn":
            name = "Dynamic"
        if name == "Spec":
            name = "Spectral"
        type_list.append(types[name])
        token_list.append(tokens[name])
        prop_list.append(props[name])
        
        TTR = token_list[i]#np.array(type_list[i])/np.sqrt(np.array(token_list[i]))
        print(name, type_list[i], prop_list[i])
        ttr_list.append(TTR)
        
    ttr_list = (np.array(ttr_list)/sum(token_list))*100
    ttr_list = list(ttr_list)
    tot_types.append(type_list)
    tot_tokens.append(token_list)
    tot_TTR.append(ttr_list)
    tot_props.append(prop_list)

indexes =  cat_name

#%%

plt.figure(figsize=(12,8))
# set width of bar
barWidth = 0.2

plt.subplot(211)
# set height of bar
bars1 = tot_props[0]
bars2 = tot_props[1]
bars3 = tot_props[2]
bars4 = tot_props[3] 
# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3] 
# Make the plot
plt.bar(r1, bars1, color='goldenrod', width=barWidth, edgecolor='white', label='bright')
plt.bar(r2, bars2, color='firebrick', width=barWidth, edgecolor='white', label='warm')
plt.bar(r3, bars3, color='royalblue', width=barWidth, edgecolor='white', label='round')
plt.bar(r4, bars4, color='forestgreen', width=barWidth, edgecolor='white', label='rough')
# Add xticks on the middle of the group bars
x= [r + barWidth for r in range(len(bars1))]
plt.xlabel('semantic categories', fontweight='bold')
plt.ylabel('% in population', fontweight='bold')
plt.xticks(x, cat_name) 
# Create legend & Show graphic
plt.legend()


plt.subplot(212)
# set height of bar
bars1 = tot_TTR[0]
bars2 = tot_TTR[1]
bars3 = tot_TTR[2] 
bars4 = tot_TTR[3] 
# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3] 
# Make the plot
plt.bar(r1, bars1, color='goldenrod', width=barWidth, edgecolor='white', label='bright')
plt.bar(r2, bars2, color='firebrick', width=barWidth, edgecolor='white', label='warm')
plt.bar(r3, bars3, color='royalblue', width=barWidth, edgecolor='white', label='round')
plt.bar(r4, bars4, color='forestgreen', width=barWidth, edgecolor='white', label='rough')
# Add xticks on the middle of the group bars
x= [r + barWidth for r in range(len(bars1))]
plt.xlabel('semantic categories', fontweight='bold')
plt.ylabel('Token (%) in corpus', fontweight='bold')
plt.xticks(x, cat_name) 
# Create legend & Show graphic
plt.legend()



plt.savefig('figure/new.eps', bbox_inches='tight')
# plt.show()

