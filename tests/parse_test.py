import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from twkbpy import decode
from util import hex_to_bytes, hex_to_stream


class DecodeTest(unittest.TestCase):

    def test_decode_point(self):
        g = decode(hex_to_stream('01000204'))
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
        g = decode(hex_to_stream('02000202020808'))
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
        g = decode(hex_to_stream('03031b000400040205000004000004030000030500000002020000010100'))
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

    def test_decode_multigeom_with_ids(self):
        g = decode(hex_to_stream('04070b0004020402000200020404'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'id': 0,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [0, 1]
                    }
                },
                {
                    'type': 'Feature',
                    'id': 1,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [2, 3]
                    }
                }
            ]
        })

    def test_decode_collection(self):
        g = decode(hex_to_stream('070402000201000002020002080a0404'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'id': 0,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [0, 1]
                    }
                },
                {
                    'type': 'Feature',
                    'id': 1,
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[4, 5], [6, 7]]
                    }
                }
            ]
        })
