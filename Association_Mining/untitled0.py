# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_mHLWoaVCL6cTuVAr3rIrkU4Z5oNSYzR
"""

from google.colab import drive
drive.mount('/content/drive')
!ls
!pwd
!cd /content/drive
print('done')

cd "/content/drive/My Drive/"

ls

import numpy as np
import pandas as pd

extractiveRecords=pd.read_csv('/content/drive/My Drive/CSC522-ALDA/RK_ALDA_PROJ/Final Submission/K-Means/extractive.csv')



new=pd.read_csv("/content/drive/My Drive/extractive.csv")











new.reset_index(drop=True,inplace=True)

new.head()

lst=[]
for i in range(new.shape[0]):
  x=new.loc[i,"extracted spy context"]
  y=x[1:len(x)-1].replace("'","").lower().split(", ")[0].split(" ")

  lst.append([j for j in y if (j not in stop)])

# lst=[]
# for i in range(no.shape[0]):
    # lst.append(no.loc[i,'extracted spy context'])

len(lst)

lst[:10]

cd '/content/new_assoc'

import apyori

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop=set(stopwords.words('english'))



def strtolist(x):
  x=x[1:len(x)-1].replace("'","").split(", ")

from apyori import apriori

assoc_mining=apriori(lst,min_confidence=0.03,min_support=0.01,max_length=10)
assoc_res=list(assoc_mining)

len(assoc_res)

assoc_res





lst1= ''
for i in range(new.shape[0]):
  x=new.loc[i,"extracted spy context"]
  y=x[1:len(x)-1].replace("'","").lower().split(", ")[0]
  print(y)
  lst1 += y
  lst1 += ' '
  # break
  # lst1.append([j for j in y if (j not in stop)])

lst1

lst1

lst1=lst1.split(" ")

lst1

lst1 = [x for x in lst1 if x!='spy' and x!='app' and x!='spying']

'spy' in lst1



from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

lst1

import matplotlib.pyplot as plt

matplotlib inline

' '.join(lst1)

lst1=lst1.remove('spy')
lst1.remove('app')

lst1.remove("spying")



wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(' '.join(lst1))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")

plt.show()

lst1=list(set(lst1))

'looking' in lst1

cooc = np.zeros((len(lst1), len(lst1)),np.float64)

for i in range(len(lst)):    
  words_in_sentence = lst[i]
  list_of_indeces = [lst1.index(word) for word in words_in_sentence]
  for index1 in list_of_indeces:
    for index2 in list_of_indeces:
        if index1 != index2:
            cooc[index1,index2] +=1

np.max(cooc)

cooc

lst1.index("spy")

ind=cooc[26].argsort()[-30:][::-1]
for j in ind:
  print(lst1[j]+" "+str(cooc[26,j]))
  # print()

cooc[26].argsort()

cooc[26].argsort()[-20:]

cooc[26].argsort()[-20:][::-1]

lst[0:10]







bgs = nltk.bigrams(['cool', 'hand', 'luke', 'paul', 'leonard', 'newman', 'january', 'september', 'he', 'quiet', 'private', 'man', 'but', 'giant', 'amongst', 'star', 'a', 'philanthropist', 'million', 'and', 'owned', 'drove', 'racecars', 'he', 'producer', 'director', 'and', 'actor', 'beyond', 'compare', 'he', 'almost', 'every', 'award', 'a', 'great', 'talent', 'one', 'rare', 'his', 'great', 'film', 'last', 'forever', 'for', 'new', 'generation', 'see', 'and', 'always', 'u', 'in', 'page', 'history', 'he', 'always', 'said', 'lucky', 'but', 'u', 'blessed', 'for', 'world', 'he', 'passed', 'almost', 'every', 'earthly', 'test', 'the', 'hole', 'in', 'the', 'wall', 'gang', 'camp', 'serving', 'child', 'ill', 'where', 'could', 'fun', 'kid', 'one', 'dream', 'fulfill', 'he', 'family', 'man', 'first', 'married', 'joanne', 'fifty', 'year', 'and', 'left', 'one', 'u', 'filled', 'memory', 'grief', 'tear', 'survived', 'joanne', 'five', 'daughter', 'his', 'son', 'scott', 'gone', 'see', 'he', 'broken', 'bound', 'earth', 'and', 'suffering', 'set', 'free', 'he', 'gone', 'much', 'better', 'place', 'and', 'i', 'bet', 'looking', 'with', 'sparkling', 'eye', 'famous', 'grin', 'and', 'saying', 'i', 'always', 'around', 'del', 'abe', 'jones', 'abeabe'])

fdist = nltk.FreqDist(bgs)
for k,v in fdist.items():
    print(k,v)

wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

pd

