#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:14:29 2020

@author: VictorRosi
"""

def lemmatization(word, lemms):

    lemmed = ""
    for index, lemm in enumerate(lemms):
        if word in lemms[lemm]:
            lemmed = lemm
            if lemmed == word:
                break

    return lemmed

#%% EMBEDDING FROM TEXT CORPUS

def embedding_token_gen(corpus_sentence, stopWord, lemms, words_emb):
    import nltk
    
    
    def lemmatization(word, lemms):
        lemmed = ""
        for index, lemm in enumerate(lemms):
            if word in lemms[lemm]:
                lemmed = lemm
                if lemmed == word:
                    break
    
        return lemmed

    # CORPUS EMBEDDING
    corpus = []   
    for index, query in enumerate(corpus_sentence):
        corpus += corpus_sentence[query]
        
    # INDEXING
    corpus_tok_list = []
    corpus_sent_list = []
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    for j, sentence in enumerate(corpus): 
        # tokenisation
        tokenized = []
        tok_tmp = []
        tokenized = tokenizer.tokenize(sentence.lower())
        for k,word in enumerate(tokenized):
            # remove stop words
            if word not in stopWord:
                # lemmatize words
                if word != '' and (len(word) > 1 or word == 'à'):
                    wrd_tmp = lemmatization(word,lemms)
                    if wrd_tmp == '':
                        wrd_tmp = word
                    if wrd_tmp in words_emb and wrd_tmp not in stopWord:
                        tok_tmp.append(wrd_tmp)
        # load a list of tokenized and clean phrases
        if tok_tmp != []:
            corpus_tok_list.append(tok_tmp)
            corpus_sent_list.append(sentence)
            
    return corpus_sent_list, corpus_tok_list

def embedding_visualization(corpus_sentence, stopWord, lemms, outputdir, model_file):
    import torch
    from torch.utils.tensorboard import SummaryWriter
    from gensim.models.keyedvectors import KeyedVectors
    import os, os.path
    import numpy as np
    
    # INIT TENSORBOARD OUTPUT FILE
    for root, dirs, files in os.walk(outputdir):
        for file in files:
            os.remove(os.path.join(root, file))
    # init writer for tensorboard
    writer = SummaryWriter(outputdir)
       
    # MODEL COMPUTE    
    model = KeyedVectors.load_word2vec_format(model_file, binary=True, encoding='utf-8')
    words_emb = model.index2word
    embeddings = [model[x] for x in words_emb]
    
    corpus_sent, corpus_token = embedding_token_gen(corpus_sentence, stopWord, lemms, words_emb)
    
    # EMBEDDING VECTORS COMPUTATION
    sentences_emb = []           
    for i, sentence in enumerate(corpus_token):
        emb_tmp = []
        emb_tmp = [model[word] for word in sentence]
        sentences_emb.append(sum(emb_tmp))
    print(len(corpus_sent), len(corpus_token))
    writer.add_embedding(np.array(sentences_emb), metadata=corpus_sent)
    writer.close()
    
    return corpus_token, corpus_sent
    
    
#%% 
    

#list_test =  embedding_token_gen(sentence_query, stopWord, lemms)

# outputdir = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/output'
# model_file = '/Users/VictorRosi/Documents/GitHub/interview_analysis/embedding/frWiki_no_phrase_no_postag_500_cbow_cut10.bin'

#%%
# embedding_visualization(sentence_query, stopWord, lemms, outputdir, model_file)






