# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 14:43:39 2015

@author: shwb
"""
import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt#, data, file_data
import Meld, Tile
from copy import deepcopy
from random import shuffle

@ddt
class MeldTest(unittest.TestCase):
    
    def setUp(self):
        aspect_ratio = 0.75
        tile_height = 133.4
        self.aMeld = Meld.Meld([], 0, 0)
        self.aMeld.addTile(Tile.Tile((0, 75), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((75, 85), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((85, 100), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((100, 210), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((210, 270), tile_height, aspect_ratio))
        self.aMeld.addTile(Tile.Tile((270, 315), tile_height, aspect_ratio))
        
    def test_construction_allows_list(self):
        aspect_ratio = 0.75
        tile_height = 133.4
        bounds = (0,75,85,100,210,270,315)
        got = Meld.Meld(bounds, tile_height, aspect_ratio)
        self.assertEqual(self.aMeld, got)
        
    def test_sortPositional(self):
        gotMeld = deepcopy(self.aMeld)
        shuffle(gotMeld.tiles)
        gotMeld.sortPositional()
        self.assertEqual(self.aMeld, gotMeld)
        
    def test_mergeRight(self):
        aCopy = deepcopy(self.aMeld)
        aCopy.mergeTileRight(0)
        expected_bounds = (0, 85)
        self.assertEqual(expected_bounds, aCopy.tiles[0].getBoundaries())
        
    def test_mergeRight_raises_exception_for_out_of_bounds(self):
        self.assertRaises(IndexError, self.aMeld.mergeTileRight, self.aMeld.getMeldLength())
        
    def test_mergeRight_raises_exception_for_nothing_to_merge(self):
        self.assertRaises(IndexError, self.aMeld.mergeTileRight, self.aMeld.getMeldLength() - 1)
        self.assertRaises(IndexError, self.aMeld.mergeTileRight, -1)

    def test_mergeLeft(self):
        aCopy = deepcopy(self.aMeld)
        aCopy.mergeTileLeft(-1)
        expected_bounds = (210, 315)
        self.assertEqual(expected_bounds, aCopy.tiles[-1].getBoundaries())
        
    def test_mergeLeft_raises_exception_for_out_of_bounds(self):
        self.assertRaises(IndexError, self.aMeld.mergeTileLeft, self.aMeld.getMeldLength())
        
    def test_mergeLeft_raises_exception_for_nothing_to_merge(self):      
        self.assertRaises(IndexError, self.aMeld.mergeTileLeft, -self.aMeld.getMeldLength())
        self.assertRaises(IndexError, self.aMeld.mergeTileLeft, 0)
        
    def test_regularize(self):
        aspect_ratio = 0.75
        tile_height = 133.4
        bounds = (0,75,85,100,210,270,315)
        exp_bounds = (0,100,210,315)
        expected = Meld.Meld(exp_bounds, tile_height, aspect_ratio)
        got = Meld.Meld(bounds, tile_height, aspect_ratio)
        got.regularize()
        exp_list = [x.getBoundaries() for x in expected.tiles]
        got_list = [x.getBoundaries() for x in got.tiles]
        self.assertEqual(exp_list, got_list)

        
if __name__ == "__main__":
    unittest.main(verbosity=2)

    