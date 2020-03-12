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
tot_values = []
tot_div = []
tot_ind = []
opt = 0
for term in terms:
    df = pd.read_excel(r"res_cat/"+ term +"_Q2_.xlsx")
    
    categories = dict.fromkeys(df["cat"].tolist())
    cat_tmp = defaultdict(list)
    cat_tmp2 = defaultdict(list)
    cat_div = defaultdict(list)
    cat_hist = defaultdict(list)
    cat = df["cat"].tolist()
    lemmas = df['lemma'].tolist()
    freq = df['freq'].tolist()
    expert = df['expert'].tolist()
    
    for index, lemm in enumerate(lemmas):
            cat_tmp[cat[index]].append(freq[index])
        
    for index, lemm in enumerate(lemmas):
            cat_tmp2[cat[index]]+=(ast.literal_eval(expert[index]))
    
    for i, keys in enumerate(set(cat_tmp)):
        if opt == 1:
            cat_hist[keys] = (sum(cat_tmp[keys])/sum(freq))*100
        else:
            numerator = len(list(dict.fromkeys(cat_tmp2[keys])))
            
            cat_hist[keys] = numerator #(numerator/32)*100
            
    for category in [ele for ind, ele in enumerate(cat,1) if ele not in cat[ind:]]:
        cat_div[category] = cat.count(category)
    
    
    values = []
    div_v = []
    ind =[]
    
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
        values.append(cat_hist[name])
        div_v.append(cat_div[name])
    
    print(div_v, values)
    ind = 1/((np.array(div_v))/np.array(values))
    
    tot_values.append(values)
    tot_div.append(div_v)
    tot_ind.append(ind)
indexes =  cat_name

#%%

plt.figure(figsize=(12,8))
# set width of bar
barWidth = 0.2

plt.subplot(311)
# set height of bar
bars1 = tot_values[0]
bars2 = tot_values[1]
bars3 = tot_values[2]
bars4 = tot_values[3] 
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


plt.subplot(312)
# set height of bar
bars1 = tot_div[0]
bars2 = tot_div[1]
bars3 = tot_div[2]
bars4 = tot_div[3] 
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
plt.ylabel('number of lemmas per category', fontweight='bold')
plt.xticks(x, cat_name) 
# Create legend & Show graphic
plt.legend()

plt.subplot(313)
# set height of bar
bars1 = tot_ind[0]
bars2 = tot_ind[1]
bars3 = tot_ind[2]
bars4 = tot_ind[3] 
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
plt.ylabel('number of lemmas per category', fontweight='bold')
plt.xticks(x, cat_name) 
# Create legend & Show graphic
plt.legend()

# plt.savefig('figure/prop.eps', bbox_inches='tight')
plt.show()

