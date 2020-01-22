#import modules
%reset
import os.path
import nltk
import json
import numpy as np
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
nltk.download('stopwords')


Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
T = ["brillant", "chaud", "rond", "rugueux"]


def load_data(word, question, Q):
    """
    Input  : path and file_name
    Purpose: loading text file
    Output : dictionnary of list of paragraphs/documents and
             title(initial 100 words considred as title of document)
    """
    with open(word+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    if question == [""] or question == []:
        question = Q

    titles = []
    document_list = []
    for index1, i in enumerate(Q):
        if i in question:
            for index2, j in enumerate(data[i]):
                document_list.append(j["answer"])
                titles.append([i, j['expertID']])
    print("Total Number of Documents:", len(document_list))

    return document_list


def preprocess_data(doc_set, word, db, ID):
    """
    Input  : document list
    Purpose: preprocess text (tokenize, removing stopwords, and stemming)
    Output : preprocessed text
    """
    # initialize regex tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # Create f_stemmer of class FrenchStemmer
    f_stemmer = FrenchStemmer()
    # list for tokenized documents in loop
    texts = []
    text = []
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

    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if i not in stopWord]
        # stem tokens
        stemmed_tokens = [f_stemmer.stem(i) for i in stopped_tokens]
        # add tokens to list
        text.append(stemmed_tokens)

    if ID is not True:
        for index, expert in enumerate(text):
            texts += text[index]
    else:
        texts = text

    return texts


def pres_result(clean_tok, ID):
    doc_freq = []
    doc_ord = []
    if ID is True:
        for index, expert in enumerate(clean_tok):
            dup = {}
            list_word = []
            for s, i in enumerate(expert):
                dup[i] = expert.count(i)
            dup = sorted(dup.items(), key=lambda t: t[1], reverse=True)
            for index, word in enumerate(dup):
                list_word.append(word[0])
            doc_ord.append(list_word)
            doc_freq.append(dup)  # si on veut un dictionnaire
    else:
        dup = {}
        list_word = []
        for s, i in enumerate(clean_tok):
            dup[i] = clean_tok.count(i)
        dup = sorted(dup.items(), key=lambda t: t[1], reverse=True)
        for index, word in enumerate(dup):
            list_word.append(word[0])
        doc_ord.append(list_word)
        doc_freq.append(dup)  # si on veut un dictionnaire

    return doc_ord



# Par expert
ID = False
word = "brillant"
doc = load_data(word, ["Q2"], Q)
clean_tok = preprocess_data(doc, word, False, ID)
res = pres_result(clean_tok, ID)

doc_fin
dup = {}
    for index, i in enumerate(test):
        print(test.count(i))
        dup[i] = test.count(i)
    duplicated = []
