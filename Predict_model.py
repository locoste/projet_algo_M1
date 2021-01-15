# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 21:04:32 2021

@author: louis
"""

import pickle

class Predict_Model():
    
    instances = {}
    
    def __init__(self, model, forecast, mots):
        self.model = model
        self.forecast = forecast
        Predict_Model.instances[mots] = self
        
    @classmethod
    def get_all_instances(cls):
        return cls.instances
        
    @classmethod
    def save_instances(cls):
        Predict_Model.save(cls)
        
    @classmethod
    def load_instances(cls):
        Predict_Model.instances = Predict_Model.load(cls)
        
        
    def save(cls) :
        with open("pickle/predict_model.pickle", 'wb') as handle:
            pickle.dump(cls.instances, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(cls) :
        with open("pickle/predict_model.pickle", 'rb') as handle:
            return(pickle.load(handle))