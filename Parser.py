# coding: utf-8
%reset
import json
import pandas as pd
import numpy as np



# from parseFunc00 import transcriptParser

with open('expert_index.json') as json_file:
    data = json.load(json_file)

Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
words = ["brillant", "chaud", "rond", "rugueux"]

word = "brillant"
path = "transcript_clean/"


def utf8Struggle(strTemp):
    strTemp = strTemp.replace('é', 'e')
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
    return strTemp


def transcriptParser(path, Q, question):
    df = pd.read_csv(path,
                     error_bad_lines=False,
                     encoding='utf8',
                     delimiter=':',
                     engine='python',
                     skip_blank_lines=True)
    # Dictionnarization
    Transcript = df.to_dict()
    # Separation of number and answers into 2 dictionaries
    Speak = Transcript['QR']
    Text = Transcript['T']
    # Prep of dictionary result that get all answers for the 6 questions.
    k = 0
    strTemp = ""
    result = {}
    for index, i in enumerate(Speak.items()):
        if i[1] == 'R' or i[1] in Q:
            if Text[index] is not None:
                strTemp += Text[index]
            else:
                if k > 0:
                    strTemp = strTemp.replace('\xa0', '')
                    strTemp = strTemp.replace('\\', '')
                    # strTemp = utf8Struggle(strTemp)
                    result[k] = strTemp
                    strTemp = ""
                k += 1
    strTemp = strTemp.replace('\xa0', '')
    strTemp = strTemp.replace('\\', '')
    # strTemp = utf8Struggle(strTemp)
    result[k] = strTemp
    loc = Q.index(question)+1
    return result[loc]
#############################


word = words[2]

for word in words:
    total = {}

    for index, question in enumerate(Q):
        Qtemp = []
        ID = []
        file = ''
        for index, expert in enumerate(data['experts']):
            file = expert["firstName"] + expert["lastName"] + "_" + word + ".txt"
            newPath = path + file
            ID = expert["expertID"]
            Qtemp.append({"expertID": ID, "answer": transcriptParser(newPath, Q, question)})
            newPath = path
            total[question] = Qtemp
    total

    jsonfile = json.dumps(total, indent=2)
    with open(word+'.json', 'w') as f_output:
                f_output.write(jsonfile)
