# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:31:47 2021

@author: louis
"""

import pandas
from fbprophet import Prophet
from Predict_model import Predict_Model
import matplotlib.pyplot as plt
import FBMethods as fm
from pandas import to_datetime
import mpld3

# df = pandas.read_csv('./coocurence_test.csv', sep = ';')

df = list()
for i in range(16,21):
    for j in range(1,13):
        date = '20%s-%s' % (str(i), str(j))
        df.append([date, 0])
df.append(['2021-1', 0])
df = pandas.DataFrame(df)
df.columns = ['ds', 'y']
df['ds'] = to_datetime(df['ds'])

# m = Prophet(weekly_seasonality=False, daily_seasonality=False)
# m.fit(df)
def prediction_graph(mots):
    plot_data_gen = {}
    for mot in mots:
        for index, value in Predict_Model.get_all_instances().items():
            tmp = index.split("_")
            if mot.split("_")[0] in tmp and mot.split("_")[1] in tmp:
                model = value.model
                forecast = value.forecast
        
                plot_data = {}
                plot_data['start'] = model.start
                plot_data['y_scale'] = model.y_scale
                plot_data['t_scale'] = model.t_scale
                plot_data['beta'] = model.params['beta']
                plot_data['forecast'] = forecast
                plot_data['history'] = model.history
                
                plot_data_gen[mot.split("_")[0]+"_"+mot.split("_")[1]] = plot_data
                
                break
    
    fig = fm.plot_components(plot_data_gen)
    plt.savefig('prophet')
    mpld3.save_html(fig, "figures/figure.html")
    return 

def prediction_only_data(df_word, mots):
    # on créer une liste de chaque mois de l'année pour l'année 2019, 2020 et 2021
    future = list()
    for i in range(19,22):
        for j in range(1,13):
            date = '20%s-%s' % (str(i), str(j))
            future.append([date])
    # On convertie cette liste en dataFrame
    future = pandas.DataFrame(future)
    # On défini la colonne du dataframe par 'ds'
    future.columns = ['ds']
    # On convertie les chaines de caractère de la colonne 'ds' en datetime 
    future['ds'] = to_datetime(future['ds'])
    
    # On défini temp_df comme étant le dataframe df
    temp_df = df
    
    # Pour chaque date(ligne) de temp_df on regarde si la date est dans le dataframe word_df
    #Si oui, on remplace le 0 de temp_df par la valeur de ord_df dans la colonne 'y'
    for index, row in temp_df.iterrows():
        for index_word, row_word in df_word.iterrows():
            if row['ds'] == to_datetime(row_word['ds']):
                temp_df.loc[index, 'y'] = row_word['y']
    
    from fbprophet.plot import plot_plotly, plot_components_plotly
    
    # On défini model comme une instance de Prophet
    model = Prophet(weekly_seasonality=False, daily_seasonality=False)
    # on entraine le modèle avec les données de temp_df.
    model.fit(temp_df)
    
    # On effectue la prédiction avec les dates du dataframe future et on définit forecast comme 
    #le dataframe contenant le résultat de la prédiction
    forecast = model.predict(future)
    
    # On créer l'instance de Predict_Model pour le couple de mot courant avec model et forecast
    Predict_Model(model, forecast, mots[0] + "_" + mots[1])
    # On sauvegarde les instances de Predict_Model dans un fichier pickle avant de renvoyer les dates 
    #et les prédictions du dataframe forecast
    Predict_Model.save_instances()
    
    return forecast[['ds', 'yhat']]