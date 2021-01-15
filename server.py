# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 09:11:46 2020

@author: louis
"""

#importation des librairies et fichier nécessaire ua bon fonctionnement de ce fichier
import flask
import os
import pandas
import pickle
import json
from flask import send_file
import Cooccurence as Cooc
import Communautes
from Predict_model import Predict_Model
import Prediction


# définition du dossier courant étant comme le dossier de ce fichier
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# définiton de la variable app qui est l'application serveur 
app = flask.Flask(__name__, static_folder="./")
app.config['APPLICATION_ROOT'] = '/Algo'


#L'ensemble des routes qui seront applé par le fontend
@app.route("/")
def get_home_page():
    return app.send_static_file("assets/Graph.html")

@app.route("/css/<file>", methods = ["GET"])
def getcssfile(file):
    return send_file("assets/css/"+file)

@app.route("/vendors/<file>")
def getvendorfile(file):
    return send_file("assets/vendors/"+file)

@app.route("/js/<file>")
def getjsfile(file):
    return send_file("assets/js/"+file)

@app.route("/images/<file>")
def getimagesfile(file):
    return send_file("assets/images/"+file)

@app.route("/json/<file>")
def getjsonfile(file):
    return send_file("assets/json/"+file)

@app.route("/fonts/Roboto/<file>")
def getfontsfile(file):
    return send_file("assets/fonts/Roboto/"+file)

@app.route("/maps/<file>")
def getmapsfile(file):
    return send_file("assets/maps/"+file)

@app.route("/json/force.json")
def get_graph():
    return send_file("force/force.json")


#cette route récupère la liste des couples de mots dont vont etre généré les graphiques 
#de prédiction et renvoie le fichier HTML contenant les graphiques
@app.route("/predict/graph", methods = ["POST"])
def get_predict_graph():
    data = json.loads(flask.request.data.decode('utf-8'))
    Prediction.prediction_graph(data["mots"])
    return send_file("figures/figure.html")

#Cette route renvoie les fichhers HTML des courbes de prédiction
@app.route("/predict/graph.html")
def get_prediction_page():
    return send_file("figures/figure.html")

# cette route renvoie la liste de l'ensemble des titres de document de la classe Document
@app.route("/graph/get_doc_list")
def get_doc_list():
    tmp = ['prediction']
    for index, value in Cooc.cooccurence.get_all_instances().items():
        tmp.extend(d[0].get_title() for i, d in value.documents.items() if d[0] != 'prediction')
    tmp = [tmp[i] for i, _ in enumerate(tmp) if tmp[i] not in tmp[:i]]
    return flask.json.dumps({'doc_list':tmp})
    
#Cette route créer le graph associé au filtrage de l'utilisateur
@app.route("/graph/set_graph")
def set_graph():
    arg = {}
    arg['start_date'] = flask.request.args.get('start_date')
    arg['end_date']=flask.request.args.get('end_date')
    arg['documents']=flask.request.args.get('documents')
    
    if arg['start_date']==None:
        arg['start_date']='2016-01'
        
    if arg['end_date'] == None:
        arg['end_date'] = '2021-12'
        
    Communautes.set_graph(arg)
    return send_file("assets/Graph.html")

#Le serveur est lancé par cette fonction qui charge dans un premier temps toutes les instances 
# de cooccurrences et models de prédiction présents dans les pickles du dossier pickle
if __name__ == "__main__":
    Cooc.cooccurence.load_instances()
    Predict_Model.load_instances()
    print("\nGo to http://localhost:10546 to see the example\n")
    #L'application tourne sur le port 10546
    app.run(port=10546) 