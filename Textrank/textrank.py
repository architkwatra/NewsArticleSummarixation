# -*- coding: utf-8 -*-
"""TextRank.ipynb

Automatically generated by Colaboratory.

"""
import json, gzip, time
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import nltk
nltk.download("stopwords")
nltk.download("punkt")

def remove_stop_words(sent, stop_words):
    sent_new=""
    for word in sent:
      if word not in stop_words:
        sent_new+=word+" "
    return sent_new[:-1]

start_time = time.time()
word_embeds = {}
f = open('/content/drive/My Drive/glove.6B.300d.txt', encoding='utf-8')

from google.colab import drive
drive.mount('/content/drive')

for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeds[word] = coefs
f.close()

csv_file = pd.read_csv("/content/drive/My Drive/extractive.csv")
text = csv_file['text']
summary = csv_file['summary']

# TextRank with cosine similarity
k=0
result_summary=[]
ground_summary=[]
not_done=[]
for row in text:
        if len(row)>7000:
            continue
        extractive=""
        article = []
        article.append(sent_tokenize(row))
        sentences=[]
        for sent in article:
            for word in sent:
                sentences.append(word)

        modified_sent = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
        modified_sent = [s.lower() for s in modified_sent]

        stop_words = stopwords.words('english')

        modified_sent = [remove_stop_words(x.split(), stop_words) for x in modified_sent]

        sent_vectors = []
        for i in modified_sent:
            if len(i)!=0:
                v = sum([word_embeds.get(w, np.zeros((300,))) for w in i.split()])/(len(i.split())+0.001)
            else:
                v = np.zeros((300,))
            sent_vectors.append(v)

        simmilarity_mat = np.zeros([len(sentences), len(sentences)])

        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i!=j:
                    simmilarity_mat[i][j] = cosine_similarity(sent_vectors[i].reshape(1, 300), sent_vectors[j].reshape(1, 300))[0, 0]

        # print(sim_mat)
        try:
            graph = nx.from_numpy_array(simmilarity_mat)
            nx.hits(graph, max_iter=500)
            scores = nx.pagerank(graph)
            # print(scores)

            ranked_sent = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
            j=0
            i=0
            while i<=len(row)*0.2:
                extractive+=ranked_sent[j][1]
                i+=len(ranked_sent[j][1])
                j+=1
            if k%1000==0:
              print(k)
            k+=1
            result_summary.append(extractive)
            ground_summary.append(summary.iloc[k])
        except:
            print("Could not convert", k)
            not_done.append(k)
            k+=1
print(time.time()-start_time)


#300d Rogue score for TextRank with Cosine Similarity
from rouge import Rouge
import matplotlib.pyplot as plt


rouge = Rouge()
res_scores=[]
for i in  range(0,len(result_summary)):
  if(len(result_summary[i])>0):
    # print(i)
    scores = rouge.get_scores(result_summary[i], ground_summary[i])
    scores=scores[0]
    svalues = list(scores.values())
    svalues = svalues[0]
    # print(svalues)
    res_scores.append([svalues['f'], svalues['p'], svalues['r']])

plt.title("Rogue")
print(len(res_scores))
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scores]
plt.scatter(range(0, len(res_scores)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()


# TextRank with BM25 similarity index
from math import log10
import re

k = 0
result_summary = []
ground_summary = []
not_done = []
for row in text:
    # print(len(row))
    if len(row) > 7000:
        continue

    extractive = ""
    article = []
    article.append(sent_tokenize(row))

    sentences = []
    for sent in article:
        for word in sent:
            sentences.append(word)
    # sent=row.split("\n\n")
    modified_sent = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    modified_sent = [s.lower() for s in modified_sent]
    temp_sent = modified_sent.copy()
    stop_words = stopwords.words('english')

    modified_sent = [remove_stop_words(x.split(), stop_words) for x in modified_sent]

    sent_scores = []

    d_words = 0
    sent_words = []
    for sentences in modified_sent:
        words = sentences.split(" ")
        for word in words:
            d_words += 1
        sent_words.append(len(words))

    sent_avg = np.array(sent_words)
    sen_avg = np.mean(sent_avg)

    sent_keyword = {}
    for sentences in modified_sent:
        temp = sentences.split(" ")
        temp = list(set(temp))
        for w in temp:
            if w not in sent_keyword:
                sent_keyword[w] = 0
            sent_keyword[w] += 1

    k1 = 1.2
    b = 0.75
    for i, sentences in enumerate(modified_sent):
        term_freq = {}
        for word in sentences.split(" "):
            if word not in term_freq:
                term_freq[word] = 0
            term_freq[word] += 1
        score = 0
        for w in term_freq.keys():
            idf = log10((len(temp_sent) - sent_keyword[w] + 0.5) / (sent_keyword[w] + 0.5))
            score += idf * (term_freq[w] * (k1 + 1)) / (term_freq[w] + k1 * (1 - b + b * (d_words / sen_avg)) + 0.25)
        sent_scores.append((i, score))

    sent_scores = sorted(sent_scores, key=lambda x: x[1], reverse=True)

    j = 0
    extractive = ""

    while i <= len(row) * 0.3:
        extractive += temp_sent[sent_scores[j][0]]
        i += len(temp_sent[sent_scores[j][0]])

        j += 1
    extractive = " ".join(extractive.split())
    result_summary.append(extractive)
    ground_summary.append(summary.iloc[k])
    k += 1
print(time.time() - start_time)

# Rogue Score for TextRank with BM25 similarity index
rouge = Rouge()
res_scores=[]
for i in  range(0,len(result_summary)):
  if(len(result_summary[i])>0):
    # print(i)
    scores = rouge.get_scores(result_summary[i], ground_summary[i])
    scores=scores[0]
    svalues = list(scores.values())
    svalues = svalues[0]
    # print(svalues)
    res_scores.append([svalues['f'], svalues['p'], svalues['r']])

plt.title("Rogue")
print(len(res_scores))
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scores]
plt.scatter(range(0, len(res_scores)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()