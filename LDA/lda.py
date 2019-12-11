# -*- coding: utf-8 -*-
"""LDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sje1fo1Z9jsmZVzGsTHAL-cjYkSip7FS
"""

from google.colab import drive
drive.mount('/content/drive')
!ls
!pwd
!cd /content/drive
print('done')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt    
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

import nltk
import re
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords=set(stopwords.words('english'))

nltk.download('wordnet')

data=pd.read_csv('/content/drive/My Drive/RK_ALDA_PROJ/Final Submission/K-Means/extractive.csv')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

dic={}
for e in stopwords:
  dic[e]=0

def preprocessing(x):
  tokens=word_tokenize(x)
  filter1 = [re.sub('[0-9]','', i) for i in tokens]
  filter2=[lemmatizer.lemmatize(w.lower()) for w in filter1 if(not w in dic and w.isalpha())]
  return filter2

import gensim
from gensim.utils import simple_preprocess

# for i in range(2):
#   x=data.loc[i,"text"].lower().split('\n')
#   y = ' '.join(x).replace('  ', ' ')
#   input_sentence = []
#   for sentence in y.split('.'):
#     input_sentence.append([sentence])
#   processed_docs = documents['headline_text'].map(preprocess)
#   processed_docs[:10]
#   dictionary = gensim.corpora.Dictionary(input_sentence)
#   count = 0
#   for k, v in dictionary.iteritems():
#     print(k, v)
#     count += 1
#     if count > 10:
#         break
#   print("LOLLLLLL\n\n\n\n")
#   dictionary.filter_extremes(no_below=0, no_above=0.01, keep_n=100000)
#   print(len(dictionary))
#   count = 0
#   for k, v in dictionary.iteritems():
#     print(k, v)
#     count += 1
#     if count > 10:
#       break

# Commented out IPython magic to ensure Python compatibility.
# Load the library with the CountVectorizer method
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline
# Helper function
def plot_10_most_common_words(count_data, count_vectorizer):
    import matplotlib.pyplot as plt
    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts+=t.toarray()[0]
    
    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x:x[1], reverse=True)[0:10]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words)) 
    
    plt.figure(2, figsize=(15, 15/1.6180))
    plt.subplot(title='10 most common words')
    sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90) 
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.show()
# Initialise the count vectorizer with the English stop words
gen_summaries=[]
for i in range(5000):
  print(i)
  input_sentence = []
  count_vectorizer = CountVectorizer(stop_words='english')
  # Fit and transform the processed titles
  input_sentence=[]
  x=data.loc[i,"text"].lower().split('\n')
  y = ' '.join(x).replace('  ', ' ')
  temp=pd.DataFrame(columns=['new'])
  for sentence in y.split('.'):
    # input_sentence.append([sentence])
    # print(inp_sentence)
    if len(sentence)>10:
      input_sentence.append([sentence])
      temp=temp.append({'new': sentence},ignore_index=True)
  # input_sentence
  # input_sentence.remove([])

  # val=data.loc[0, 'text']


  # temp=temp.append({'new': val},ignore_index=True)
  # print(temp)
  count_data = count_vectorizer.fit_transform(temp['new'])
  # # # Visualise the 10 most common words
  # plot_10_most_common_words(count_data, count_vectorizer)

  import warnings
  warnings.simplefilter("ignore", DeprecationWarning)
  # Load the LDA model from sk-learn
  from sklearn.decomposition import LatentDirichletAllocation as LDA
  topics=[]
  # Helper function
  def print_topics(model, count_vectorizer, n_top_words):
      words = count_vectorizer.get_feature_names()
      for topic_idx, topic in enumerate(model.components_):
          # print("\nTopic #%d:" % topic_idx)
          # print(topic)
          topics.append([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
          # print(" ".join([words[i]
          #                 for i in topic.argsort()[:-n_top_words - 1:-1]]))
          
  # Tweak the two parameters below
  number_topics = 4
  number_words = 5
  # Create and fit the LDA model
  lda = LDA(n_components=number_topics, n_jobs=-1)
  lda.fit(count_data)
  # Print the topics found by the LDA model
  
  print_topics(lda, count_vectorizer, number_words)
  topics=topics_preprocess(topics)
  intersection=extract_sentences(input_sentence,topics)
  
  dic=makeDict(intersection)
  # print(dic)
  gen_summaries.append(predict(dic, input_sentence))

rouge = Rouge()
res_scores1=[]
res_scores2=[]
res_scoresL=[]
for i in  range(0,5000):
  if(len(gen_summaries[i])<6000 and len(data['summary'].iloc[i])<6000):
    scores = rouge.get_scores(gen_summaries[i], data['summary'].iloc[i])
    scores_1=scores[0]
    svalues_1 = list(scores_1.values())
    svalues_1 = svalues_1[0]
    res_scores1.append([svalues_1['f'], svalues_1['p'], svalues_1['r']])

    scores_2=scores[0]
    svalues_2 = list(scores_2.values())
    svalues_2 = svalues_2[1]
    # print(svalues)
    res_scores2.append([svalues_2['f'], svalues_2['p'], svalues_2['r']])

    scores_l=scores[0]
    svalues_l = list(scores_l.values())
    svalues_l = svalues_l[2]
    # print(svalues)
    res_scoresL.append([svalues_l['f'], svalues_l['p'], svalues_l['r']])


print("\n **************** ROGUE 1 ********************** \n")

plt.title("Rogue")
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scores1]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores1)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()

plt.title("Rogue")
# plt.plot([pt[1] for pt in res_scores],label = 'Precission')
plot_vals = [pt[1] for pt in res_scores1]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores1)), plot_vals,label = 'Precission')
plt.legend()
plt.show()

plt.title("Rogue")
plot_vals = [pt[2] for pt in res_scores1]

print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores1)), plot_vals,label = 'Recall')
plt.legend()
plt.show()


print("\n **************** ROGUE 2 ********************** \n")

plt.title("Rogue")
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scores2]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores2)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()

plt.title("Rogue")
# plt.plot([pt[1] for pt in res_scores],label = 'Precission')
plot_vals = [pt[1] for pt in res_scores2]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores2)), plot_vals,label = 'Precission')
plt.legend()
plt.show()

plt.title("Rogue")
plot_vals = [pt[2] for pt in res_scores2]

print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores2)), plot_vals,label = 'Recall')
plt.legend()
plt.show()


print("\n **************** ROGUE L ********************** \n")

plt.title("Rogue")
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scoresL]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scoresL)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()

plt.title("Rogue")
# plt.plot([pt[1] for pt in res_scores],label = 'Precission')
plot_vals = [pt[1] for pt in res_scoresL]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scoresL)), plot_vals,label = 'Precission')
plt.legend()
plt.show()

plt.title("Rogue")
plot_vals = [pt[2] for pt in res_scoresL]

print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scoresL)), plot_vals,label = 'Recall')
plt.legend()
plt.show()

# plt.title('Box-Plot of Recall')
# plot_vals = [pt[2] for pt in res_scores]
# plt.boxplot(plot_vals)

# plt.title('Box-Plot of Precission')
# plot_vals = [pt[1] for pt in res_scores]
# plt.boxplot(plot_vals)

# plt.title('Box-Plot of F-Score')
# plot_vals = [pt[0] for pt in res_scores]
# plt.boxplot(plot_vals)

print("\n **************** ROGUE 1 ********************** \n")

plt.title("Rogue")
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scores1]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores1)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()

plt.title("Rogue")
# plt.plot([pt[1] for pt in res_scores],label = 'Precission')
plot_vals = [pt[1] for pt in res_scores1]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores1)), plot_vals,label = 'Precission')
plt.legend()
plt.show()

plt.title("Rogue")
plot_vals = [pt[2] for pt in res_scores1]

print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores1)), plot_vals,label = 'Recall')
plt.legend()
plt.show()


print("\n **************** ROGUE 2 ********************** \n")

plt.title("Rogue")
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scores2]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores2)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()

plt.title("Rogue")
# plt.plot([pt[1] for pt in res_scores],label = 'Precission')
plot_vals = [pt[1] for pt in res_scores2]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores2)), plot_vals,label = 'Precission')
plt.legend()
plt.show()

plt.title("Rogue")
plot_vals = [pt[2] for pt in res_scores2]

print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scores2)), plot_vals,label = 'Recall')
plt.legend()
plt.show()


print("\n **************** ROGUE L ********************** \n")

plt.title("Rogue")
# plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
plot_vals = [pt[0] for pt in res_scoresL]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scoresL)), plot_vals,label = 'F-Score')
plt.legend()
plt.show()

plt.title("Rogue")
# plt.plot([pt[1] for pt in res_scores],label = 'Precission')
plot_vals = [pt[1] for pt in res_scoresL]
print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scoresL)), plot_vals,label = 'Precission')
plt.legend()
plt.show()

plt.title("Rogue")
plot_vals = [pt[2] for pt in res_scoresL]

print(np.mean(plot_vals))
plt.scatter(range(0, len(res_scoresL)), plot_vals,label = 'Recall')
plt.legend()
plt.show()

def topics_preprocess(topics):
  t=""
  for element in topics:
    t+=" ".join(element)
    t+=" "
  topics = t.split(" ")
  topics.remove('')
  topics = list(set(topics))
  return topics

def extract_sentences(input_sentence,topics):
  sentences_ind=[]
  dic = {}
  for j in range(len(input_sentence)):
    inter=0
    for i in range(len(topics)):
      temp = set(topics[i]).intersection(set(input_sentence[j][0].split(' ')))
      inter = max(inter, len(temp))
    sentences_ind.append(inter)
  # sentences_ind = set(sentences_ind)
  
  return sentences_ind

# intersection = extract_sentences(input_sentence, topics)

def makeDict(intersection):
  dic = {}
  for i in range(len(intersection)):
    if intersection[i] in dic:
      dic[intersection[i]].append(i)
    else:
      dic[intersection[i]] = [i]
  return dic

def predict(dic, input_sentence):
  predicted_sentences = []
  keys = sorted(dic.keys())
  keys.sort(reverse = True)
  indices = set()
  for key in keys:
    br = False
    for index in dic[key]:
      indices.add(index)
    
  for index in indices:
    predicted_sentences.append(input_sentence[index])
    if len(predicted_sentences) > 3:
      br = True
      break
    if br:
      break
  t = ''
  for element in predicted_sentences:
    t+=" ".join(element)
    t+=". "

  return t

rouge = Rouge()
res_scores=[]
for i in  range(0,5000):
  # if(len(gen_summaries[i])<6000 and len(extractiveRecords['summary'].iloc[i])<6000):
  scores = rouge.get_scores(gen_summaries[i], data['summary'].iloc[i])
  scores=scores[0]
  svalues = list(scores.values())
  svalues = svalues[0]
  # print(svalues)
  res_scores.append([svalues['f'], svalues['p'], svalues['r']])

# plt.title("Rogue")
# print(len(res_scores))
# # plt.plot([pt[0] for pt in res_scores],label = 'F-Score')
# plot_vals = [pt[0] for pt in res_scores]
# plt.scatter(range(0, len(res_scores)), plot_vals,label = 'F-Score')
# plt.legend()
# plt.show()

# plt.title("Rogue")
# print(len(res_scores))
# # plt.plot([pt[1] for pt in res_scores],label = 'Precission')
# plot_vals = [pt[1] for pt in res_scores]
# plt.scatter(range(0, len(res_scores)), plot_vals,label = 'Precission')
# plt.legend()
# plt.show()

# plt.title("Rogue")
# print(len(res_scores))
# plot_vals = [pt[2] for pt in res_scores]
# plt.scatter(range(0, len(res_scores)), plot_vals,label = 'Recall')
# plt.legend()
# plt.show()

plt.title('Box-Plot of Recall')
plot_vals = [pt[2] for pt in res_scores]
plt.boxplot(plot_vals)

plt.title('Box-Plot of Precission')
plot_vals = [pt[1] for pt in res_scores]
plt.boxplot(plot_vals)

plt.title('Box-Plot of F-Score')
plot_vals = [pt[0] for pt in res_scores]
plt.boxplot(plot_vals)

pip install rouge

from rouge import Rouge

