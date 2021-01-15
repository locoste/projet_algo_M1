import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpld3 import plugins
from datetime import datetime
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import (AutoDateLocator, AutoDateFormatter, MonthLocator, num2date)

def plot_components(plot_data):
    print(len(plot_data))
    
    compt = 0
    fig = plt.figure(constrained_layout=False, figsize=[20,3*len(plot_data)])
    gs = gridspec.GridSpec(ncols=1, nrows=len(plot_data), figure=fig)
    for index, value in plot_data.items():
        ax = fig.add_subplot(gs[compt,0])
        ax.set_title(index.split("_")[0] + "-" + index.split("_")[1])
        tooltip1, tooltip2 = plot_forecast(history=value['history'],
                                           forecast=value['forecast'],
                                           ax=ax)
        plugins.connect(fig, tooltip1); plugins.connect(fig, tooltip2) # Connect our tooltip plugins to the figure
        compt += 1

    fig.tight_layout() # Automatically adjusts subplot params so that the subplot(s) fits into the figure area
    return fig # Return the full figure

'''
    Dessine le plot de Prédiction sur un ax donné
'''
def plot_forecast(history, forecast, ax):
    # Conversion des dates en pydatetime pour les abscisses
    forecast_t = forecast['ds'].dt.to_pydatetime() # Dates des prédictions
    history_t = history['ds'].dt.to_pydatetime() # Dates des vraies données
    # Dessin d'une zone d'incertitude pour la prédiction
    ax.fill_between(forecast_t, forecast['yhat_lower'], forecast['yhat_upper'], color='red', alpha=0.2) # (dates prédites, prédiction minimale, prédiction maximale, couleur, transparence)
    # Dessin des courbes et récupération des points pour les tooltips(')

    p1 = ax.plot(history_t, history['y'], 'o-', ms=5, c='m')
    p2 = ax.plot(forecast_t, forecast['yhat'], 'o-', ms=5, c='r')
    # Formattage propre à Matplotlib
    locator = AutoDateLocator(interval_multiples=False)
    formatter = AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # Options pour la grille de fond
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    # Déclaration des noms pour l'abscisse et l'ordonnée
    ax.set_xlabel('Months', labelpad=10)
    ax.set_ylabel('Topic Frequency', labelpad=10)
    # Création des tooltips avec mpld3.plugins
    labels = ['%s-%s : %s' % (date.strftime("%B"), date.strftime("%Y"), str(int(y))) for date,y in zip(history_t, history['y'])]
    tooltip1 = plugins.PointLabelTooltip(p1[0], labels=labels, hoffset=10, voffset=10)
    labels = ['%s-%s : %s' % (date.strftime("%B"), date.strftime("%Y"), str(int(y))) for date,y in zip(forecast_t, forecast['yhat'])]
    tooltip2 = plugins.PointLabelTooltip(p2[0], labels=labels, voffset=10, hoffset=10)
    return tooltip1, tooltip2
