# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 11:39:21 2015

@author: shwb
"""
class Tile(object):
    def __init__(self, (xlimits), height, aspect_ratio):
        self.leftborder = xlimits[0]
        self.rightborder = xlimits[1]
        self.identity = None
        self.height = height
        self.aspect_ratio = aspect_ratio # width / height
    
    # overriding equality operator    
    def __eq__(self, otherTile):
        if isinstance(otherTile, self.__class__):
            return otherTile.identity == self.identity and \
                    self.getBoundaries() == otherTile.getBoundaries()
        else:
            return False
            
    # overriding inequality operator
    def __ne__(self, otherTile):
        return not self.__eq__(otherTile)
    
    # getters    
    def getBoundaries(self):
        return (self.leftborder, self.rightborder)
        
    def getWidth(self):
        return self.rightborder - self.leftborder
        
    def getAspectRatio(self):
        return self.aspect_ratio
        
    def which(self):
        return self.identity
    
    # setters    
    def setId(self,identity):
        self.identity = identity
        
    def setBoundaries(self,left,right):
        self.leftborder = left
        self.rightborder = right
        
    
        
    
    
