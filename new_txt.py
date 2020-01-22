# coding: utf-8
%reset
import json
import numpy as np


Q = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
T = ["brillant","chaud","rond","rugueux"]



def exp_text_q(word, question, Q, n, db):
    # load json.file
    with open(word+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    ID = [expert['expertID'] for expert in data[question]]
    answers = [expert['expertID']+" : "+expert['answer'] for expert in data[question]]
    text = '\n'.join(str(elem) for elem in answers)

    with open("transcription_Q/"+ word+"_"+question+".txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)


def exp_text_ID(word, ID, Q, n, db):
    # load json.file
    with open(word+'.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    for item, i in enumerate(data[question]):
        ID = i['expertID']
        answers = i['answer']
        with open("transcription_Q_ID/"+ID+"_"+ word+"_"+question+".txt", "w", encoding="utf-8") as text_file:
            text_file.write(text)


for term in T:
    for question in Q:
        exp_text_ID(term, question, Q, 1, True)
