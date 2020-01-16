# coding: utf-8
%reset
import json
import numpy as np
import nltk


word = "brillant"
Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
experts = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
           "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
           "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]


with open(word+'.json') as json_file:
    data = json.load(json_file)

# Q_tot = np.full((len(experts), len(data)), "")

Q_tot = {}
for index1, i in enumerate(Q):
    Q_tot[i] = []
    for index2, j in enumerate(data[i]):
        print(index1, index2)
        Q_tot[i].append(j["answer"])
        # Q_tot[index2][index1] = j["answer"]

for index, i in enumerate(Q_tot["Q1"]):
# commande typique
# Q_tot["Q2"][0]+Q_tot["Q3"][0]
