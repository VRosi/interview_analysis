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

def lemmatization(word, lemms):
    lemmed = ""
    for index, lemm in enumerate(lemms):
        if word in lemms[lemm]:
            lemmed = lemm
            if lemmed == word:
                break

    return lemmed


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

    with open('lemm_file.json', encoding="utf-8") as json_file:
        lemms = json.load(json_file)

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
    for index, word in enumerate(tokenized):
        if index > 0:
            if word == tokenized[index-1]:
                tokenized.pop(index)
    if n > 1:  # for n-grams
        tokenized = n_gram(tokenized, n)

    # get rid of stopwords + stem
    stemmer = FrenchStemmer()  # stem machine from Snowball
    res = ''
    if n > 1:  # for n-grams
        for index, i in enumerate(tokenized):
            x = i.split(' ')
            # check if one of the words is in the stopWord list
            comp = any(elem in x for elem in stopWord)
            # check if both words are in the exception list
            exep = all(elem in exStopWord for elem in x)
            if comp is False and exep is False and x[-1] not in exStopWord:

                res = lemmatization(i, lemms)
                # if the joint expression finds no match
                if res == '':
                    for index, w in enumerate(x):
                        if lemmatization(w, lemms) == '':
                            print(w)
                            x[index] = stemmer.stem(w)
                    res = ' '.join(x)
                stemmatized.append(res)
    else:
        for index, word in enumerate(tokenized):
            if word not in stopWord:
                res = lemmatization(word, lemms)
                if res == '':
                    res = stemmer.stem(word)
                    if res == '':
                        res = word
                        print(res)
                    else:
                        stemmatized.append(res)
                        if res != '':
                            stemmatized.append(res)
                else:
                    stemmatized.append(res)

    # kill duplicates
    for index, i in enumerate(set(stemmatized)):
        duplicated[i] = stemmatized.count(i)
    # sort from most to least used
    finalized = sorted(duplicated.items(), key=lambda t: t[1], reverse=True)
    return finalized, tokenized




result, stem = freqWord_tot("chaud", ["Q5"], Q, 1, True)
result[0:100]

# sentence query
result, tok = freqWord_tot("chaud", [""], Q, 1, True)
# Query : add "*" at the end of word if you want use it as stem
q_word = "chaleur"
n_L = 2;
n_R = 4;
sentence = []
for index, word in enumerate(tok):
    if q_word[-1] == '*':
        if q_word[0:-1] in word or q_word[0:-1] == word:
            temp = ' '.join(tok[index-n_L:index+1+n_R])
            sentence.append(temp)
    else:
        if q_word == word:
            temp = ' '.join(tok[index-n_L:index+1+n_R])
            sentence.append(temp)
sentence

# # query
# search = ""
# stemmer = FrenchStemmer()
# search2 = stemmer.stem(search)
# result = freqWord_tot("chaud", [""], Q, 1, True)
# print(search, [item for item in result if item[0] == search2])
