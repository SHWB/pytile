# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 11:29:41 2015

@author: shwb
"""
from Tile import Tile


class Meld(object):
    def __init__(self, boundary_list, height, ratio, image = None):
        self.image = image
        self.tiles = []
        for i in range(len(boundary_list) - 1):
            left = boundary_list[i]
            right = boundary_list[i+1]
            self.addTile(Tile((left, right), height, ratio))            
    
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
        current_tile.setBoundaries(prev_tile.leftborder, current_tile.rightborder)
        del(self.tiles[index-1])
        
    def regularize(self):
        tolerance = .9
        i = 0
        while i < len(self.tiles)-2:
            try:
                if self.tiles[i].isTooThin(tolerance):
                    self.mergeTileRight(i)
                else:
                    i += 1
            except IndexError as e:
                print(e.message)                
                return

        try:
            if self.tiles[-1].isTooThin(tolerance):
                    self.mergeTileLeft(-1)
        except IndexError as e:
                print(e.message)
                return
                        
        
