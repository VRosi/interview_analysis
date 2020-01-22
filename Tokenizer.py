# coding: utf-8
%reset
import json
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import FrenchStemmer

# tokenizer = nltk.RegexpTokenizer(r'\w+')
# stemmer = FrenchStemmer()

Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]

def freqWord_tot(word, question, Q, n, db):
    # load json.file
    with open(word+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    # dictionnary of Questions for everyone.
    Q_tot = {}  # dictionnary with all answers for each question
    for index1, i in enumerate(Q):
        Q_tot[i] = []
        for index2, j in enumerate(data[i]):
            Q_tot[i].append(j["answer"])

    if question == [""] or question == []:
        question = Q

    # call function for tokenization/stem/dup
    result = freqWord_q(word, question, Q_tot, n, db)
    return result


def n_gram(list, n):
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[list[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def freqWord_q(word, question, Q_tot, n, db):
    text = ""
    tokenized = stemmatized = finalized = []
    duplicated = {}

    # load stop words in a file
    file = "stopwords-fr.txt"
    stopFile = open(file, 'r', encoding="utf-8")
    yourResult = np.array([line.split('\n')
                           for line in stopFile.readlines()])[:, 0]
    stopWord = list(yourResult)
    stopWord.append(word)

    if db is True:
        file = "dataset_stopwords.txt"
        stopFile = open(file, 'r', encoding="utf-8")
        yourResult = np.array([line.split('\n')
                               for line in stopFile.readlines()])[:, 0]
        dbStopWord = list(yourResult)
        stopWord += dbStopWord

    if n > 1:
        # load exception words in a file
        file = "minus_stopwords.txt"
        stopFile = open(file, 'r', encoding="utf-8")
        temp = [line.split(' ') for line in stopFile.readlines()]
        exStopWord = temp[0]
        for word in exStopWord:
            if word in stopWord:
                stopWord.remove(word)

    # group all answers in 1 string
    for qnum in question:
        for index, i in enumerate(Q_tot[qnum]):
            text += i
    # tokenisation
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokenized = tokenizer.tokenize(text.lower())
    if n > 1:  # for n-grams
        tokenized = n_gram(tokenized, n)

    # get rid of stopwords + stem
    stemmer = FrenchStemmer()  # stem machine from Snowball
    if n > 1:  # for n-grams
        for index, i in enumerate(tokenized):
            x = i.split(' ')
            # check if one of the words is in the stopWord list
            comp = any(elem in x for elem in stopWord)
            # check if both words ar in the exception list
            exep = all(elem in exStopWord for elem in x)
            if comp is False and exep is False:
                res = ' '.join([stemmer.stem(w) for w in x])
                stemmatized.append(res)
    else:
        for index, i in enumerate(tokenized):
            if i not in stopWord:
                stemmatized.append(stemmer.stem(i))
    print(stemmatized)
    # kill duplicates
    for index, i in enumerate(set(stemmatized)):
        duplicated[i] = stemmatized.count(i)
    print(duplicated)
    # sort from most to least used
    finalized = sorted(duplicated.items(), key=lambda t: t[1], reverse=True)
    return finalized



result = freqWord_tot("rond", ["Q2"], Q, 1, True)
result[0:100]
fin = []

for word in result[0:70]:
    strTemp = word[0].replace('é', 'e')
    strTemp = strTemp.replace('è', 'e')
    strTemp = strTemp.replace('ë', 'e')
    strTemp = strTemp.replace('ê', 'e')
    strTemp = strTemp.replace('É', 'E')
    strTemp = strTemp.replace('à', 'a')
    strTemp = strTemp.replace('â', 'a')
    strTemp = strTemp.replace('ü', 'u')
    strTemp = strTemp.replace('û', 'u')
    strTemp = strTemp.replace('ù', 'u')
    strTemp = strTemp.replace('ï', 'i')
    strTemp = strTemp.replace('î', 'i')
    strTemp = strTemp.replace('ç', 'c')
    strTemp = strTemp.replace('Ç', 'C')
    strTemp = strTemp.replace('ô', 'o')
    fin.append([strTemp, word[1]])

import csv
with open("res/rugueux_2_2.csv", "w", newline="") as output:
    writer = csv.writer(output)
    for val in fin:
        writer.writerow(val)


# query
search = "cornet"
stemmer = FrenchStemmer()
search2 = stemmer.stem(search)
result = freqWord_tot("chaud", [""], Q, 1, True)
print(search, [item for item in result if item[0] == search2])
