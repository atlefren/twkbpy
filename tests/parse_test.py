import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from twkbpy import decode
from util import hex_to_bytes


class DecodeTest(unittest.TestCase):

    def test_decode_point(self):
        g = decode(hex_to_bytes('01000204'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [1, 2]
                    }
                }
            ]
        })

    def test_decode_linestring(self):
        g = decode(hex_to_bytes('02000202020808'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[1, 1], [5, 5]]
                    }
                }
            ]
        })

    def test_decode_polygon(self):
        g = decode(hex_to_bytes('03031b000400040205000004000004030000030500000002020000010100'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]], [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
                    }
                }
            ]
        })
