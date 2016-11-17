import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from twkbpy import decode
from util import hex_to_bytes, hex_to_stream


class GeneratorTest(unittest.TestCase):

    def test_decode_point(self):
        generator = decode(hex_to_stream('01000204'))
        first = next(generator)
        self.assertEqual(first, {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [1, 2]
            }
        })
        with self.assertRaises(StopIteration):
            next(generator)

    def test_decode_multigeom_with_ids(self):
        generator = decode(hex_to_stream('04070b0004020402000200020404'))
        first = next(generator)
        self.assertIsNotNone(first)

        second = next(generator)
        self.assertIsNotNone(second)

        with self.assertRaises(StopIteration):
            next(generator)
