# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:27:56 2021

@author: louis
"""

import pickle

class cooccurence():
    
    instances = {}
    
    # nb_occurence --> {'01/01/2016':12, '01/02/2016':64, ....}
    # documents --> {'01/01/2016':[document1, document2], '01/02/2016':[document3], ....}
    
    def __init__(self, mot1, mot2, nb_occurence, documents):
        self.mots = [mot1, mot2]
        self.nb_occurence = nb_occurence
        self.documents = documents
        cooccurence.instances[mot1+"_"+mot2] = self
    
    def get_mots(self):
        return self.mots
    
    def get_occurence(self):
        return self.nb_occurence
    
    def set_occurence(self, nb_occurence):
        self.nb_occurence = nb_occurence
        
    @classmethod
    def get_all_instances(cls):
        return cls.instances
    
    @classmethod
    def save_instances(cls):
        cooccurence.save(cls)
        
    @classmethod
    def load_instances(cls):
        cooccurence.instances = cooccurence.load(cls)
    
    @classmethod
    def set_all_instances(cls, instances):
        cls.instances = instances
    
    def save(cls) :
        with open("pickle/coocurence_instances.pickle", 'wb') as handle:
            pickle.dump(cls.instances, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(cls) :
        with open("pickle/coocurence_instances.pickle", 'rb') as handle:
            return(pickle.load(handle))
        
    def __str__(self):
        return str(self.mots) + ', occurrence: ' + str(self.nb_occurence) + ', documents: ' + str(self.documents)