# -*- coding: utf-8 -*-

from geojson_transforms import transforms
from read_buffer import read_buffer


def byte_gen(stream):
    while True:
        a = stream.read(1)
        if a == '':
            raise StopIteration
        yield bytearray(a)[0]


class Decoder:

    def decode(self, stream):

        ta_struct = {
            'stream': byte_gen(stream),
            'refpoint': [None] * 4
          }

        features = []
        while True:
            try:
                res = read_buffer(ta_struct)
            except StopIteration:
                break
            transformer = transforms[ta_struct['type']]
            ndims = ta_struct['ndims']
            if 'geoms' in res:
                features += transformer(res['geoms'], res['ids'], ndims)
            else:
                features.append({
                    'type': 'Feature',
                    'geometry': transformer(res, ndims)
                })

        return {
            'type': 'FeatureCollection',
            'features': features
        }
