import sys
sys.path.insert(0, 'src')
import unittest
import detect_clusters

class TestSequenceFunctions(unittest.TestCase):

    def test_whatever(self):
        clusters_count = detect_clusters.count( None )
        self.assertEqual(0, clusters_count)

if __name__ == '__main__':
    unittest.main()