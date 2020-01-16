# coding: utf-8


import json
import pandas as pd
import numpy as np


with open('expert_index.json') as json_file:
    data = json.load(json_file)
    data

num = 13
wordIndex = 2
data['experts'][num]['expertID']

path = "transcript_clean/"
firstName = data['experts'][num]['firstName']
lastName = data['experts'][num]['lastName']
words = ["brillant", "chaud", "rond", "rugueux"]
Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
file = firstName + lastName + "_" + words[wordIndex] + ".txt"

############## Parsing
df = pd.read_csv(path + file,
                 error_bad_lines=False,
                 encoding='utf8',
                 delimiter=':',
                 engine='python',
                 skip_blank_lines=True)
df
# Dictionnarization
Transcript = df.to_dict()
# Separation of number and answers into 2 dictionaries
Speak = Transcript['QR']
Text = Transcript['T']

###############
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
                result[k] = strTemp
                strTemp = ""
            k += 1
            print(index, k)

strTemp = strTemp.replace('\xa0', '')
strTemp = strTemp.replace('\\', '')
result[k] = strTemp
result[1]
Speak

type(data["experts"])

Q1= []
for index, expert in enumerate(data['experts']):
    print(index, expert["expertID"], expert["firstName"], expert["lastName"])
    ID = expert["expertID"]
    Q1.append({"expertID": ID})
    print(Q1)
Q1


# Q1 = {}
# Q1['userID'] = data['experts'][num]['expertID']
# Q1['answer'] = result[1]
#
# Q2 = {}
# Q2['userID'] = data['experts'][num]['expertID']
# Q2['answer'] = result[2]
#
# Q3 = {}
# Q3['userID'] = data['experts'][num]['expertID']
# Q3['answer'] = result[3]
#
# Q4 = {}
# Q4['userID'] = data['experts'][num]['expertID']
# Q4['answer'] = result[4]
#
# Q5 = {}
# Q5['userID'] = data['experts'][num]['expertID']
# Q5['answer'] = result[5]
#
# Q6 = {}
# Q6['userID'] = data['experts'][num]['expertID']
# Q6['answer'] = result[6]
#
# Q5
