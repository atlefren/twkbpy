# -*- coding: utf-8 -*-

from geojson_transforms import transforms
from read_buffer import read_buffer


class Decoder:

    def decode(self, buffer):

        ta_struct = {
            'buffer': buffer,
            'cursor': 0,
            'buffer_length': len(buffer),
            'refpoint': [None] * 4
          }

        features = []
        while ta_struct['cursor'] < ta_struct['buffer_length']:
            res = read_buffer(ta_struct)
            transformer = transforms[ta_struct['type']]
            ndims = ta_struct['ndims']
            if 'geoms' in res:
                pass
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
