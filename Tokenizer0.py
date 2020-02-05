# coding: utf-8

import json
import pathlib
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import FrenchStemmer




#%%
def load_file(word, db):
    """
    This function load the verbatims for a WORD and QUESTION(s)
    INPUT :  - word
             - question of interest
             - list of question
    OUTPUT : - dictionnary of answers
             - stopwords list (with or without dataset related words)
    """

    
    path = str(pathlib.Path(__file__).parent.absolute())
    
    # load json.file
    with open(word+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    # dictionnary of questions for everyone.
    data_dic = {}  # dictionnary with all answers for each question
    for index, i in enumerate(data):
        key = ''.join(["Q", str(index+1)])
        data_dic[key] = []
        for index2, j in enumerate(data[key]):
            data_dic[key].append(j["answer"])

    # load stop words in a file
    file = "stopwords-fr.txt"
    stopFile = open(file, 'r', encoding="utf-8")
    yourResult = np.array([line.split('\n')
                           for line in stopFile.readlines()])[:, 0]
    stopWord = list(yourResult)
    stopWord.append(word)

    # load lemmatization file
    with open('lemm_file.json', encoding="utf-8") as json_file:
        lemms = json.load(json_file)

    # If True, remove all words related to the dataset of sounds
    if db is True:
        file = "dataset_stopwords.txt"
        stopFile = open(file, 'r', encoding="utf-8")
        yourResult = np.array([line.split('\n')
                               for line in stopFile.readlines()])[:, 0]
        dbStopWord = list(yourResult)
        stopWord += dbStopWord

    return data_dic, stopWord, lemms



def n_gram(list, n):
    """
    This function use the zip function to help us generate n-grams
    Concatentate the tokens into ngrams and return
    OUTPUT : - n-gram string
    """
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




def freqNGram(word, question, n, db):
    Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
    text = ""
    tokenized = []
    lemmatized = []
    finalized = []
    unduplicated = {}

    # import verbatims, stopwords and lemm list
    data_dic, stopWord, lemms = load_file(word, db)

    # group all answers in 1 string
    if question == [""] or question == []:
        question = Q
    for qnum in question:
        for index, i in enumerate(data_dic[qnum]):
            text += i

    # tokenisation
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokenized = tokenizer.tokenize(text.lower())
    if n > 1:  # for n-grams
        for index, word in enumerate(tokenized):
            if index > 0:
                if word == tokenized[index-1]:
                    tokenized.pop(index)
        tokenized = n_gram(tokenized, n)
        # load exception words in a file
        file = "minus_stopwords.txt"
        stopFile = open(file, 'r', encoding="utf-8")
        temp = [line.split(' ') for line in stopFile.readlines()]
        exStopWord = temp[0]
        for word in exStopWord:
            if word in stopWord:
                stopWord.remove(word)

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
                    for index, word in enumerate(x):
                        if lemmatization(word, lemms) == '':
                            x[index] = word
                        else:
                            x[index] = lemmatization(word, lemms)
                    res = ' '.join(x)
                lemmatized.append(res)
    else:
        for index, word in enumerate(tokenized):
            if word not in stopWord:
                res = lemmatization(word, lemms)
                if res == '':
                    res = word
                lemmatized.append(res)

    # kill duplicates
    for index, i in enumerate(set(lemmatized)):
        unduplicated[i] = lemmatized.count(i)
    # sort from most to least used
    finalized = sorted(unduplicated.items(), key=lambda t: t[1], reverse=True)
    return finalized, tokenized, lemmatized

def contQuery(tokenized_list, q_word, n_L, n_R):
    # context query for 1-gram and 2-gram
    # Query : add "*" at the end of q_word if you want use it as stem
    context = []
    k = 0
    for index, word in enumerate(tokenized_list):
        if len(q_word.split(' ')) > 1:
            if q_word.split(' ')[0] == word and q_word.split(' ')[1] == tokenized_list[index+1]:
                temp = ' '.join(tokenized_list[index-n_L:index+2+n_R])
                context.append(temp)
                k += 1
        if q_word[-1] == '*':
            if q_word[0:-1] in word or q_word[0:-1] == word:
                temp = ' '.join(tokenized_list[index-n_L:index+1+n_R])
                context.append(temp)
                k += 1
        else:
            if q_word == word:
                temp = ' '.join(tokenized_list[index-n_L:index+1+n_R])
                context.append(temp)
                k += 1
    print("{} iterations of {} in context : \n"  .format(k, q_word))
    print('\n'.join(map(str, context)))
    return context


# Generate excel files with results
def generate_df(word, db, Qlist):
    writer = pd.ExcelWriter(word+'.xlsx', engine='xlsxwriter')
    for index, Q in enumerate(Qlist):
        Qkey = [Q]
        for n in [1, 2]:
            print(n)
            result, tokenized, lemmatized = freqNGram(word, Qkey, n, db)
            df = pd.DataFrame(result, columns =[word, 'F'])
            df.to_excel(writer, index=False, sheet_name=word+'_'+str(n)+'_'+Q)
    writer.save()

#%%
    
quest = "Q2","Q5"
n = 1
word = "rond"
    
result, tokenized, lemmatized = freqNGram(word, ["Q2","Q5"], n, True)
#context = contQuery(tokenized, "net*", 15, 15
# generate_df("rugueux", True, [""])

#%%
path_j = './embedding/corpus_lemm/'

result_dict = dict(result)
jsonfile = json.dumps(result_dict, indent=2)
with open(path_j + word + "_Q2Q5_"+ str(n) +'.json', 'w') as f_output:
    f_output.write(jsonfile)
