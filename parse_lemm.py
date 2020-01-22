#import modules
%reset
import os.path
import nltk
import json
import pandas as pd
import numpy as np
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
nltk.download('stopwords')

def Parser(path):
    df = pd.read_csv(path,
                     error_bad_lines=False,
                     encoding='utf8',
                     delimiter=' -> ',
                     engine='python',
                     skip_blank_lines=True)
    # Dictionnarization
    Transcript = df.to_dict()
    # Separation of number and answers into 2 dictionaries
    lemm = Transcript['LEMM']
    wordlist = Transcript['WOOR']
    # Prep of dictionary result that get all answers for the 6 questions.
    k = 0
    ref = []
    coll = []
    result = {}
    for index, i in enumerate(lemm.items()):
        result[i[1]] = wordlist[index].split(",")
    return Transcript, result
    # strTemp = strTemp.replace('\xa0', '')
    # strTemp = strTemp.replace('\\', '')
    # # strTemp = utf8Struggle(strTemp)
    # result[k] = strTemp
    # loc = Q.index(question)+1
    # return result[loc]
#############################

file = "lefff-antconclex-f.txt"

Transcript, result = Parser(file)

jsonfile = json.dumps(result, indent=2)
with open("lemm_file"+'.json', 'w') as f_output:
            f_output.write(jsonfile)
