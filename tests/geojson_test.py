import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from twkbpy import to_geojson
from util import hex_to_bytes, hex_to_stream


class GeoJsonTest(unittest.TestCase):

    def test_decode_point(self):
        g = to_geojson(hex_to_stream('01000204'))
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
        g = to_geojson(hex_to_stream('02000202020808'))
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
        g = to_geojson(hex_to_stream('03031b000400040205000004000004030000030500000002020000010100'))
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
        g = to_geojson(hex_to_stream('04070b0004020402000200020404'))
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
        g = to_geojson(hex_to_stream('070402000201000002020002080a0404'))
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

    def test_decoce_polygon_with_holes(self):
        g = to_geojson(hex_to_stream('03031b000400040205000004000004030000030500000002020000010100'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]],
                            [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
                        ]
                    }
                }
            ]
        })

    def test_decode_multipoint_no_ids(self):
        # SELECT encode(ST_AsTWKB('MULTIPOINT((1 2), (3 4))'::geometry, 0, 0, 0, true, true), 'hex')
        g = to_geojson(hex_to_stream('040309020404040202040404'))
        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [1.0, 2.0]
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [3.0, 4.0]
                    }
                }
            ]
        })
    
    def test_decode_multilinestring_no_ids(self):
        # SELECT encode(ST_AsTWKB('MULTILINESTRING((1 2, 3 4), (5 6, 7 8))'::geometry, 0, 0, 0, true, true), 'hex')
        g = to_geojson(hex_to_stream('05030f020c040c0202020404040204040404'))

        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[1.0, 2.0], [3.0, 4.0]]
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[5.0, 6.0], [7.0, 8.0]]
                    }
                }
            ]
        })

    def test_decode_multipolygon_no_ids(self):
        # SELECT encode(ST_AsTWKB('MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)), ((10 10, 11 10, 11 11, 10 11, 10 10)))'::geometry, 0, 0, 0, true, true), 'hex')
        g = to_geojson(hex_to_stream('06031d0016001602010500000200000201000001010514140200000201000001'))

        self.assertEqual(g, {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[[10.0, 10.0], [11.0, 10.0], [11.0, 11.0], [10.0, 11.0], [10.0, 10.0]]]
                    }
                }
            ]
        })
