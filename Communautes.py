# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:26:37 2020

@author: louis
"""

"""
Set the graph
"""
import igraph
from Cooccurence import cooccurence
import Display
import pickle
from pandas import to_datetime
from datetime import datetime


def set_graph(arg):
    #On crée un graph vide
    g = igraph.Graph()
    #On appelle la fonction de création des liens avec les options de filtrage 
    #passé en paramettre de la fonction. Celle-ci renvoie un nouveau graph avec les liens et noeuds
    g = set_edges(g, arg['start_date'], arg['end_date'], arg['documents'])
    # On envoie le nouveau graph vers la fonction de détection de communautées qui va renvoyer 
    # une liste de cluster que l'on met dans la variable i
    i = detection_by_infomap(g)
    #on envoie g et i vers la fonction qui va générer le fichier json nécessaire à l'affichage du graph
    Display.init_graph(g, i)
    return g

def set_vertices(g, mot, documents):
    tmp = []
    # on boucle sur l'ensemble des documents du dictionnaire passé en paramètre
    for index, doc in documents.items():
            for d in doc:
                #si l'élement n'est pas une chaine de caractère 'prédiction' donc 
                #une instance de Document on ajoute le titre du document à la liste temporaire
                #Sinon on ajoute le mot prédiction
                if d != 'prediction':
                    tmp.append(str(d.get_title()))
                else:
                    tmp.append(d)
    #On créer le noeud avec le mot et la liste de document créer au préalable avant de retourner le nouveau graph
    g.add_vertices(mot, {"mot":mot, "documents": tmp})
    return g

def set_edges(g, start_date, end_date, documents):
    #word est la liste des mots qui sont présent dans le graph
    word = []
    # Pour chaque instance de cooccurrence on vérifie que la somme des cooccurrences comprise 
    # entre les deux dates entré par l'utilisateur
    for index, value in cooccurence.get_all_instances().items():
        if sum(d for i, d in value.nb_occurence.items() if to_datetime(i) >= datetime.strptime(start_date, '%Y-%m') and to_datetime(i) <= datetime.strptime(end_date, '%Y-%m'))>0 and (documents in value.documents or documents == None):
            #Si l'un des deux mots n'est pas dans le graph on le crée
            if value.mots[0] not in word:
                g = set_vertices(g, value.mots[0], value.documents)
                word.append(value.mots[0])
            if value.mots[1] not in word:
                g = set_vertices(g, value.mots[1], value.documents)
                word.append(value.mots[1])
            #on créer les attributs du lien
            kwds = {"weight":sum(d for i, d in value.nb_occurence.items() if to_datetime(i) >= datetime.strptime(start_date, '%Y-%m') and to_datetime(i) <= datetime.strptime(end_date, '%Y-%m'))}
            #On créer le lien avant de retourner le graph rempli
            g.add_edge(str(value.mots[0]),str(value.mots[1]),**kwds)

    return g
# on fait une détection de communautés sur le graph et on retourne la liste des clusters 
#contenant les noeuds concerné par chaque cluster
def detection_by_infomap(g):
    i = g.community_infomap(edge_weights="weight", trials=20)
    return i
