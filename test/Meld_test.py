# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 14:43:39 2015

@author: shwb
"""
import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data, file_data
import Meld, Tile
import numpy as np
from copy import deepcopy
from random import shuffle

@ddt
class MeldTest(unittest.TestCase):
    
    def setUp(self):
        aspect_ratio = 0.75
        tile_height = 133.4
        self.aMeld = Meld.Meld()
        self.aMeld.addTile(Tile.Tile((0, 75), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((75, 85), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((85, 100), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((100, 210), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((210, 270), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((270, 315), tile_height, aspect_ratio)) 
        
    def test_sort(self):
        gotMeld = deepcopy(self.aMeld)
        shuffle(gotMeld.tiles)
        gotMeld.sortPositional()
        self.assertEqual(self.aMeld, gotMeld)
        
    def test_MergeRight(self):
        self.aMeld.mergeTileRight(0)
        expected_bounds = (0, 85)
        self.assertEqual(expected_bounds, self.aMeld.tiles[0].getBoundaries())
        
if __name__ == "__main__":
    unittest.main(verbosity=2)

    