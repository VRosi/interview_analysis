#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json

"""
Created on Thu Feb 20 15:00:39 2020

@author: VictorRosi

-----------

This code allows to plot an histogram and a word cloud 
based on words frequencies obtained through .json files 

Just run it and see :-)

Values to update below

"""


term = 'chaud' # Investigated term
question = 'Q2'   # Q2 or Q5 
cutoff_wc = 1     # Cutoff frequency of terms/concepts in corpus (default = 1) for word cloud plot
cutoff_hist = 3   # Cutoff frequency of terms/concepts in corpus (default = 3) for histogram plot


#%% LOAD / INDEX
# Path of json files
path = '/Users/VictorRosi/Documents/GitHub/interview_analysis/corpus_lemm/'
unigram_file = path+term+'_'+question+'_.json'


# Open unigram/frequency file
with open(unigram_file) as json_file:
    uni_data = json.load(json_file)

cloud_dict = {}
for index, lemm in enumerate(set(uni_data)):
    if uni_data[lemm]['freq'] >= cutoff_wc:
        cloud_dict[lemm] = uni_data[lemm]['freq']


#%% PLOT WORDCLOUD
        
wordcloud = WordCloud(font_path='/System/Library/Fonts/AmaticSC-Bold.ttf', width=1600, height=800, background_color="white")
wordcloud.generate_from_frequencies(frequencies=cloud_dict)
plt.figure(figsize=(10,5)) # plt.figure(figsize=(20,10))
plt.tight_layout(pad=2)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


#%% PLOT HISTOGRAM  

word_list = sorted(cloud_dict.items(), key=lambda t: t[1], reverse=True)
plot_list = [word for word in word_list if word[1] >= cutoff_hist]
indexes, values = list(zip(*plot_list))
bar_width = 0.35
plt.figure(figsize=(8,8))
plt.barh(indexes, values)
plt.gca().invert_yaxis()
plt.title('Words frequencies for ' +term+ "'s definition")
plt.show()