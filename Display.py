# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 00:33:31 2021

@author: louis
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:26:14 2020

@author: louis
"""

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import json
import random
import pickle

import networkx as nx
from networkx.readwrite import json_graph

def init_graph(g, i):
    #On créer un graph networkX
    G = nx.Graph()
    #Pour chaque noeud du graph igraph, on créé le meme dans  le graph NetworkX
    for v in  g.vs:
        G.add_nodes_from([(v.index,{"mot":v['name'], "documents":v["documents"]})])
    #On défini r comme une fonction qui génère un random entre 0 et 255
    r = lambda: random.randint(0,255)
    attr = {}
    # pour chaque cluster on défini une couleur qu'on va spécifier pou_r chaque noeud du cluster
    for clust in i:
        color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
        for clu_node in clust:
            # print(clu_node)
            attr[clu_node] = {'color':color}
        nx.set_node_attributes(G, attr)
    #Pour chaque lien du graph igraph, on créé le meme dans le graph NetworkX
    for e in g.es:
        G.add_edge(e.source, e.target, weight = e["weight"])
    #On génère le fichier JSON  du graph et on le sauvegarde dans le dossier force fichier force.json
    d = json_graph.node_link_data(G)
    json.dump(d, open("force/force.json", "w"))
    return d