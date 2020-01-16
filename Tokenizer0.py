# coding: utf-8
%reset
import json
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import FrenchStemmer
# from Parser import utf8Struggle


word = "brillant"
Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
experts = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
           "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
           "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]

# get stop words in a file
file = "stopwords-fr.txt"
stopFile = open(file, 'r', encoding="utf-8")
yourResult = np.array([line.split('\n') for line in stopFile.readlines()])[:,0]
stopWord = list(yourResult)

tokenizer = nltk.RegexpTokenizer(r'\w+')
stemmer = FrenchStemmer()

with open(word+'.json', encoding="utf-8") as json_file:
    data = json.load(json_file)

# Q_tot = np.full((len(experts), len(data)), "")
Q_tot = {}
for index1, i in enumerate(Q):
    Q_tot[i] = []
    for index2, j in enumerate(data[i]):
        Q_tot[i].append(j["answer"])
        # Q_tot[index2][index1] = j["answer"]

Q1 = ""

Q1_tok = Q1_stop = Q1_stem = Q_fin = []

Q_dup = Q_dup2 = {}


for index, i in enumerate(Q_tot["Q2"]):
    Q1 += i
    # commande typique
    # Q_tot["Q2"][0]+Q_tot["Q3"][0]

# tokenisation
Q1_tok = tokenizer.tokenize(Q1.lower())
Q1_tok
# get rid of stopwords
for index, i in enumerate(Q1_tok):
    if i not in stopWord:
        Q1_stop.append(i)

Q1_stop

for i in Q1_stop:
    if i not in stopWord:
        Q1_stem.append(i)
# Q1_stem += [stemmer.stem(w) for w in Q1_stop]
# Q1_stem += [stemmer.stem(w) for w in Q1_tok if not w in stopWord]
Q1_stem

for index, i in enumerate(set(Q1_stem)):
    Q_dup[i] = Q1_stem.count(i)

for index, i in enumerate(set(Q1_stem)):
    Q_dup2[i] = Q1_stop.count(i)

Q_dup = sorted(Q_dup.items(), key=lambda t: t[1], reverse=True)
Q_dup
