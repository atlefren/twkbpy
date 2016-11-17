import math

import constants
from protobuf import unzigzag, read_varsint64, read_varint64


def read_pa(ta_struct, npoints):

    ndims = ta_struct['ndims']
    factors = ta_struct['factors']
    coords = [None] * (npoints * ndims)

    for i in range(0, npoints):
        for j in range(0, ndims):
            ta_struct['refpoint'][j] += read_varsint64(ta_struct)
            coords[ndims * i + j] = ta_struct['refpoint'][j] / factors[j]

    '''
    # calculates the bbox if it hasn't it
    if (ta_struct.include_bbox && !ta_struct.has_bbox) {
      for (i = 0; i < npoints; i++) {
        for (j = 0; j < ndims; j++) {
          var c = coords[j * ndims + i]
          if (c < ta_struct.bbox.min[j]) {
            ta_struct.bbox.min[j] = c
          }
          if (c > ta_struct.bbox.max[j]) {
            ta_struct.bbox.max[j] = c
          }
        }
      }
    }
    '''
    return coords


def parse_point(ta_struct):
    return read_pa(ta_struct, 1)


def parse_line(ta_struct):
    npoints = read_varint64(ta_struct)
    return read_pa(ta_struct, npoints)


def parse_polygon(ta_struct):
    coordinates = []
    nrings = read_varint64(ta_struct)
    for ring in range(0, nrings):
        coordinates.append(parse_line(ta_struct))
    return coordinates


def read_objects(ta_struct):
    type = ta_struct['type']
    for i in range(0, ta_struct['ndims'] + 1):
        ta_struct['refpoint'][i] = 0

    if type == constants.POINT:
        return parse_point(ta_struct)

    if type == constants.LINESTRING:
        return parse_line(ta_struct)

    if type == constants.POLYGON:
        return parse_polygon(ta_struct)

    raise TypeError('Unknown type: %s' % type)


def read_buffer(ta_struct):
    has_z = 0
    has_m = 0

    # geometry type and precision header
    flag = ta_struct['buffer'][ta_struct['cursor']]
    ta_struct['cursor'] += 1

    precision_xy = unzigzag((flag & 0xF0) >> 4)
    ta_struct['type'] = flag & 0x0F
    ta_struct['factors'] = [None] * 4
    precision_xy = math.pow(10, precision_xy)
    ta_struct['factors'][0] = precision_xy
    ta_struct['factors'][1] = precision_xy

    # Metadata header
    flag = ta_struct['buffer'][ta_struct['cursor']]
    ta_struct['cursor'] += 1

    ta_struct['has_bbox'] = flag & 0x01
    ta_struct['has_size'] = (flag & 0x02) >> 1
    ta_struct['has_idlist'] = (flag & 0x04) >> 2
    ta_struct['is_empty'] = (flag & 0x10) >> 4

    extended_dims = (flag & 0x08) >> 3

    # the geometry has Z and/or M coordinates
    if extended_dims:
        extended_dims_flag = ta_struct['buffer'][ta_struct.cursor]
        ta_struct.cursor += 1

        # Strip Z/M presence and precision from ext byte
        has_z = (extended_dims_flag & 0x01)
        has_m = (extended_dims_flag & 0x02) >> 1
        precision_z = (extended_dims_flag & 0x1C) >> 2
        precision_m = (extended_dims_flag & 0xE0) >> 5

        # Convert the precision into factor
        if has_z:
            ta_struct['factors'][2] = math.pow(10, precision_z)
        if has_m:
            ta_struct['factors'][2 + has_z] = math.pow(10, precision_m)
        # store in the struct
        ta_struct['has_z'] = has_z
        ta_struct['has_m'] = has_m

    ndims = 2 + has_z + has_m
    ta_struct['ndims'] = ndims

    if ta_struct['has_size']:
        ta_struct['size'] = read_varint64(ta_struct)

    if ta_struct['has_bbox']:
        bbox = [None] * (ndims * 2)
        for i in range(0, ndims):
            min = read_varsint64(ta_struct)
            max = min + read_varsint64(ta_struct)
            bbox[i] = min
            bbox[i + ndims] = max
        ta_struct['bbox'] = bbox

    return read_objects(ta_struct)
