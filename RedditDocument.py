# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 08:57:03 2020

@author: louis
"""

from Document import Document

# classe fille permettant de modéliser un Document Reddit
#

class RedditDocument(Document):
    
    def __init__(self, date, title,
                 author, text, url, num_comments):        
        # Document.__init__(self, date, title, author, text, url)
        # ou : 
        super(self, date, title, author, text, url)
        self.num_comments = num_comments
        self.source = "Reddit"
        
    def get_num_comments(self):
        return self.num_comments

    def getType(self):
        return "reddit"
    
    def __str__(self):
        #return(super().__str__(self) + " [" + self.num_comments + " commentaires]")
        return Document.__str__(self) + " [" + str(self.num_comments) + " commentaires]"