#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Apr  1 14:49:13 2020

@author: julien et antoine 
"""

# package permettant d'incrémenter l'identifiant unique à attribuer à un document
#import itertools

#
# classe mère permettant de modéliser un Document (au sens large)
#

from gensim.summarization.summarizer import summarize
import re

class Document():
    
    # constructor
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
    
    # getters
    
    def get_author(self):
        return self.author

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        return self.source
        
    def get_text(self):
        return self.text

    def __str__(self):
        return "Document " + self.getType() + " : " + self.title
    
    def __repr__(self):
        return self.title

    def sumup(self,ratio):
        try:
            auto_sum = summarize(self.text,ratio=ratio,split=True)
            out = " ".join(auto_sum)
        except:
            out =self.title            
        return out
    
    def getType(self):
        pass
    
    def summarizeText(self):
        return summarize(self.text)
    
    def dataCleaning(self):
        #Mise en minuscule de l'attribut text de tous les documents
        newText = self.text.lower()
        # suppression de toutes les expressions entre crochets
        newText=re.sub('\[.*?\]','',newText) 
        # suppression de toutes les expressions entre accolades
        newText=re.sub('\{.*?\}','',newText) 
        # suppression de toutes les expressions entre parenthèses
        newText=re.sub('\(.*?\)+','',newText) 
        #Suppresssion de la ponctuation et de ceratains caractères spéciaux
        newText = re.sub('[.,\,,!,?,%,*,&,²,~,\{,\},+,;,/]','',newText)
        # suppression des 's
        newText = re.sub('(\'s)|(\')','',newText) 
        # suppression de tous les chiffres qui sont seuls
        newText=re.sub('^[0-9]+$','',newText)
        newText=re.sub('(\s\d+\s|^\d+\s|\s\d+$)','',newText)
        # suppression des expressions en rapport avec des dates ou des n-ièmes
        newText = re.sub('([0-9]+)(?:st|nd|rd|th)','',newText)
        
        return newText
    
