# coding: utf-8
%reset
import json
import numpy as np
import pandas as pd
import nltk
# from Parser import utf8Struggle


word = "brillant"
Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
experts = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
           "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
           "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]

# file = "stopwords-fr.txt"
# df = pd.read_csv(file,
#                  error_bad_lines=False,
#                  encoding='utf8',
#                  engine='python',
#                  skip_blank_lines=True)
# # Dictionnarization
# Transcript = df.to_dict()
# Transcript = Transcript["word"]
# print(Transcript)
# df



with open(word+'.json', encoding="utf-8") as json_file:
    data = json.load(json_file)

# Q_tot = np.full((len(experts), len(data)), "")

Q_tot = {}
for index1, i in enumerate(Q):
    Q_tot[i] = []
    for index2, j in enumerate(data[i]):
        print(index1, index2)
        Q_tot[i].append(j["answer"])
        # Q_tot[index2][index1] = j["answer"]

Q1 = ""

for index, i in enumerate(Q_tot["Q1"]):
    Q1 += i
# commande typique
# Q_tot["Q2"][0]+Q_tot["Q3"][0]
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokenizer.tokenize(Q1)
