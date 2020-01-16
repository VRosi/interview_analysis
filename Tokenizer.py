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

def freqWord_tot(word, question, Q, n):
    # load json.file
    with open(word+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    # dictionnary of Questions for everyone.
    Q_tot = {} # dictionnary with all answers for each question
    for index1, i in enumerate(Q):
        Q_tot[i] = []
        print(i)
        for index2, j in enumerate(data[i]):
            Q_tot[i].append(j["answer"])

    # call function for tokenization/stem/dup
    result = freqWord_q(question, Q_tot, n)
    return result


def n_gram(list, n):
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[list[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def freqWord_q(question, Q_tot, n):
    text = ""
    tokenized = stemmatized = finalized = []
    duplicated = {}

    # load stop words in a file
    file = "stopwords-fr.txt"
    stopFile = open(file, 'r', encoding="utf-8")
    yourResult = np.array([line.split('\n') for line in stopFile.readlines()])[:,0]
    stopWord = list(yourResult)

    print(len(stopWord))

    if n > 1:
        # load exception words in a file
        file = "minus_stopwords.txt"
        stopFile = open(file, 'r', encoding="utf-8")
        temp = [line.split(' ') for line in stopFile.readlines()]
        exStopWord = temp[0]
        for word in exStopWord:
            if word in stopWord:
                stopWord.remove(word)
    print(len(stopWord))

    # group all answers in 1 string
    for index, i in enumerate(Q_tot[question]):
        text += i

    # tokenisation
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokenized = tokenizer.tokenize(text.lower())
    if n > 1: # for n-grams
        tokenized = n_gram(tokenized, n)

    # get rid of stopwords + stem
    stemmer = FrenchStemmer() # stem machine from Snowball
    if n > 1: # for n-grams
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

    # kill duplicates
    for index, i in enumerate(set(stemmatized)):
        duplicated[i] = stemmatized.count(i)

    # sort from most to least used
    finalized = sorted(duplicated.items(), key=lambda t: t[1], reverse=True)
    return finalized

result = freqWord_tot("rugueux","Q6", Q, 2)
result
