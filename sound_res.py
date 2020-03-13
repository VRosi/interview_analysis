#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import math
import matplotlib.pyplot as plt

term = "rugueux"

file_loc="sounds/"+ term +".xlsx"

df = pd.read_excel(r"sounds/"+ term +".xlsx")

# instruments = ["violon","alto","violoncelle","contrebasse","flute","piccolo","flute_alto","clarinette","clarinette_basse","basson","hautbois","cor_anglais","saxophone","trompette",'cor','trombone','tuba','glockenspiel','xylophone','vibraphone','marimba','piano','guitare','accordeon']
dyn = ["pp","mf","ff"]

names = df["name"].tolist()
name_dic = list(dict.fromkeys(df["name"].tolist()))
instruments = df["instrument"].tolist()
play_techs= df["pt"].tolist()
pitchs = df["pitch"].tolist()
dyns = df["dynamic"].tolist()

res_obj = []

dims = [instruments,play_techs,pitchs,dyns]


dim = play_techs

for name in set(name_dic):
    tmp_obj = []
    indices = [i for i, x in enumerate(names) if x == name]
    #tmp_obj = [dim[i] for i in indices]
    for i in indices:
        if isinstance(dim[i],str):
            for j in dim[i].split('.'):
                tmp_obj.append(j)
    tmp_obj = list(dict.fromkeys(tmp_obj))
    res_obj += tmp_obj
    

obj_dict = {}      
obj_dict = {i:res_obj.count(i) for i in set(res_obj)}


#%% PLOT HISTOGRAM  
cutoff = 0.33

word_list = sorted(obj_dict.items(), key=lambda t: t[1], reverse=True)
plot_list = [word for word in word_list if word[1] >= round(cutoff*len(name_dic))]
indexes, values = list(zip(*plot_list))
bar_width = 0.35
plt.figure(figsize=(8,8))
plt.bar(indexes, values)
plt.title('Words frequencies for ' +term+ "'s definition")
plt.show()


#%% COMBINATION SOURCE / PLAYTECH
dim1 = instruments
dim2 = play_techs

query = "basson"
sound = []
for i in range(len(dim1)):
    print(dim1[i])
    if dim1[i] == query:
        if isinstance(dim2[i],str):
            for j in dim2[i].split('.'):
                sound.append(query+'_'+str(j))
                
obj_dict = {}      
obj_dict = {i:sound.count(i) for i in set(sound)}


#%% CHECK 
sound_list = []
for i in range(len(dim1)):
    sound_tmp = ""
    if isinstance(play_techs[i],str):
            for pt in play_techs[i].split('.'):
                if isinstance(pitchs[i],str):
                    for pitch in pitchs[i].split('.'):
                        if isinstance(dyns[i],str):
                            for dyn in dyns[i].split('.'):
                                sound_tmp += instruments[i]+'_'+pt+'_'+pitch+'_'+dyn
                                sound_list.append(sound_tmp)
                                sound_tmp = ""
    
    
obj_dict = {i:sound_list.count(i) for i in set(sound_list)}
