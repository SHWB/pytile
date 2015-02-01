# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 11:29:41 2015

@author: shwb
"""

class Meld(object):
    def __init__(self):
        self.image = None
        self.tiles = []
        
    # override equality operator
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.tiles == other.tiles
        else:
            return False
            
    # override inequality operator
    def __ne__(self, other):
        return not self.__eq__(other)
        
    # getters
    def getTileList(self):
        return self.tiles
    
    def getMeldLength(self):
        return len(self.tiles)
    
    def addTile(self, aTile):
        self.tiles.append(aTile)
    
    # setters
    def attachImage(self, image):
        self.image = image
    
    
    def sortPositional(self):
        self.tiles.sort(key = lambda x: x.leftborder, reverse = False)
     
    def mergeTileRight(self, index):
        size = len(self.tiles)
        if index >= size or index < -size:
            raise IndexError("Index out of bounds")
        elif index == size - 1 or index == -1:
            raise IndexError("Cannot merge: nothing on the right")
        current_tile = self.tiles[index]
        next_tile = self.tiles[index+1]
        current_tile.setBoundaries(current_tile.leftborder,next_tile.rightborder)
        del(self.tiles[index+1])
        
    def mergeTileLeft(self,index):
        size = len(self.tiles)
        if index >= size or index < -size:
            raise IndexError("Index out of bounds")
        elif index == 0 or index == -size:
            raise IndexError("Cannot merge: nothing on the left")
        current_tile = self.tiles[index]
        prev_tile = self.tiles[index-1]
        current_tile.setBoundaries(prev_tile.leftborder,current_tile.rightborder)
        del(self.tiles[index-1])
        
        
        
