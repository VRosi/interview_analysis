# coding: utf-8
%reset
import json
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import FrenchStemmer
from Tokenizer import freqWord_q
from Tokenizer import freqWord_tot

Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]

result = freqWord_tot("brillant","Q5", Q)
result


#     # dictionnary of Questions for everyone.
#     Q_tot = {} # dictionnary with all answers for each question
#         Q_tot[question] = []
#         i = Q.index(question)
#         for index2, j in enumerate(data[question]):
#             Q_tot[question].append(j["answer"])
#
# question = "Q2"
# Q.index(question)


file = "stopwords-fr.txt"
stopFile = open(file, 'r', encoding="utf-8")
yourResult = np.array([line.split('\n') for line in stopFile.readlines()])[:,0]
stopWord = list(yourResult)

file = "minus_stopwords.txt"
stopFile = open(file, 'r', encoding="utf-8")
temp = [line.split(' ') for line in stopFile.readlines()]
exStopWord = temp[0]
