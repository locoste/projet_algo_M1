#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020

@author: julien and antoine
"""

################################## Déclaration des classes ##################################

import datetime as dt

from Document import Document
from Corpus import Corpus
from Predict_model import Predict_Model

import Cooccurence as Cooc
import Prediction

import praw

import urllib.request
import xmltodict

import pandas
from pandas import to_datetime

import nltk
nltk.download()
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from gensim.parsing.preprocessing import STOPWORDS


################################## Création du Corpus ##################################

corpus = Corpus("Corona")


reddit = praw.Reddit(client_id='xxlBX29KI1Z6-g', client_secret='1VlCkdcsggAWx4KnD7JKK5g5Jlplqg', user_agent='TD-Algo')
hot_posts = reddit.subreddit('Corona').hot(limit=100)
for post in hot_posts:
    datet = dt.datetime.fromtimestamp(post.created)
    txt = post.title + ". "+ post.selftext
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = Document(datet,
                   post.title,
                   post.author_fullname,
                   txt,
                   post.url)
    corpus.add_doc(doc)

url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

for i in docs:
    datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
    try:
        author = [aut['name'] for aut in i['author']][0]
    except:
        author = i['author']['name']
    txt = i['title']+ ". " + i['summary']
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\r', ' ')
    doc = Document(datet,
                   i['title'],
                   author,
                   txt,
                   i['id']
                   )
    corpus.add_doc(doc)

print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))

# print()

# print("Corpus trié par titre (4 premiers)")
# res = corpus.sort_title(4)
# print(res)
    
# print()

# print("Corpus trié par date (4 premiers)")
# res = corpus.sort_date(4)
# print(res)

# print()

# print("Enregistrement du corpus sur le disque...")
# corpus.save("Corona.crp")

# search = corpus.search('COVID-19', 15)
# print(search)

#%% Importations des Stopwords en Anglais Et Fonction de sélection des Adjectifs, Noms, Verbes et Adverbes



#Pourquoi utiliser un Tokeniser plutôt que de split(" ") le texte d'un document ?
# Le tokeniser a des propriétés qui fait qu'on ne peut pas avoir la chaîne '' comme
#étant un token. Avec une chaine '', la Lemmatisation plante.
tokenizer = nltk.RegexpTokenizer(r'\w+')

stopwords = set()
stopwords.update(nltk.corpus.stopwords.words('english'))
all_stopwords = STOPWORDS.union(stopwords)


# Fonction qui va servir à identifier la nature du mot (verbe, nom, ...)
def get_wordnet_pos(word) :
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tags = {'J' : wordnet.ADJ,
            'N' : wordnet.NOUN,
            'V' : wordnet.VERB,
            'R' : wordnet.ADV}
    return tags.get(tag, wordnet.NOUN)

lemmatizer = WordNetLemmatizer()

for docu in corpus.collection.values():
    
    #On résume le texte du document
    #docu.text = docu.summarizeText()
    #On applique la fonction dataCleaning au texte du document
    text_Clean = docu.dataCleaning()
    #On transforme le texte en une liste de Tokens
    list_words= tokenizer.tokenize(text_Clean)
    
    # Après la transformation en Tokens, certains mots comme covid19 donne "covid" et "19"
    #D'où : Nécessité de supprimer tous les chiffres une 2ieme fois !
    regex = re.compile(r'^[0-9]+$')
    list_words = [i for i in list_words if not regex.search(i)]
    
    #On applique la suppression des Stopwords
    list_words = [word for word in list_words if word not in all_stopwords]
    #On applique la Lemmatisation
    list_words = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in list_words]
    
    year_month = docu.date.strftime('%Y-%m')
    #Je passe en revue chaque 2 mots qui cooccurent dans le document 
    for ind in range(len(list_words)-1):
        mot1 = list_words[ind]
        mot2 = list_words[ind+1]
        
        allInstances = Cooc.cooccurence.get_all_instances() #Dictionnaire contenant toutes les cooccurences
        
        #On vérifie si la cooccurence mot1+"_"+mot2 est déjà créée ou pas
        if mot1+"_"+mot2 in allInstances: 
            #On vérifie si le year_month actuel existe déjà dans le dict nb_occurence
            if year_month in allInstances[mot1+"_"+mot2].nb_occurence:
                allInstances[mot1+"_"+mot2].nb_occurence[year_month]+=1
                #En ce qui concerne le dict document, on vérifie si le document actuel se trouve
                #dans la liste des documents du mois donné(car le mois peut rester le mm mais 
                #le document lui, est différent)
                if docu not in allInstances[mot1+"_"+mot2].documents[year_month]:
                    allInstances[mot1+"_"+mot2].documents[year_month].append(docu)
                
            else: #Sinon on crée une nouvelle clé year_month avec coe val 1 dans le dict cooccurence de l'objet courant
                allInstances[mot1+"_"+mot2].nb_occurence[year_month]=1
                #En ce qui concerne le dict document, on crée une  nouvelle clé year_month avec coe val,
                #une liste contenant docu
                allInstances[mot1+"_"+mot2].documents[year_month]=[docu]
        else:
            nb_occurence = {year_month : 1} #création du dictionnaire du nb de coocccurences
            documents = {year_month : [docu]}
            newInstance = Cooc.cooccurence(mot1, mot2, nb_occurence, documents)


# ont charge toutes les isntances de cooccurrence et on défini un compteur à 0
allInstances = Cooc.cooccurence.get_all_instances()
cpt = 0
# Pour chaque instance, on effectue une prédiction du nombre de cooccurrence à venir
for cooc in allInstances.values():
    pred = Prediction.prediction_only_data(pandas.DataFrame(cooc.nb_occurence.items(), columns = ['ds', 'y']), cooc.mots)
    # On incrémente l'instance de cooccurrence avec les données de prédiction
    for index, value in pred.iterrows():
        cooc.nb_occurence[to_datetime(value['ds'])] =round(value['yhat'])
        cooc.documents[to_datetime(value['ds'])] = ['prediction']
    # OIn sauvegarde toutes les instances de la classe Cooccurrence et on incrémente le compteur de 1
    Cooc.cooccurence.save_instances()
    cpt+=1
    print(cpt)
    print('-----------------------------------')
