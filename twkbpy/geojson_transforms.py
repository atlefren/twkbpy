# -*- coding: utf-8 -*-
import itertools

import constants


type_map = {}
type_map[constants.POINT] = 'Point'
type_map[constants.LINESTRING] = 'LineString'
type_map[constants.POLYGON] = 'Polygon'


# Create GeoJSON Geometry object from TWKB type and coordinate array
def create_geometry(type, coordinates):
    return {
        'type': type_map[type],
        'coordinates': coordinates
    }


# TWKB flat coordinates to GeoJSON coordinates
def to_coords(coordinates, ndims):
    coords = []
    for i in range(0, len(coordinates), ndims):
        pos = []
        for c in range(0, ndims):
            pos.append(coordinates[i + c])
        coords.append(pos)
    return coords


def create_point(coordinates, ndims):
    return create_geometry(constants.POINT, to_coords(coordinates, ndims)[0])


def create_linestring(coordinates, ndims):
    return create_geometry(constants.LINESTRING, to_coords(coordinates, ndims))


def create_polygon(coordinates, ndims):
    coords = [to_coords(c, ndims) for c in coordinates]
    return create_geometry(constants.POLYGON, coords)


def create_feature(type, coordinates, id, ndims):
    feature = {
        'type': 'Feature',
        'geometry': transforms[type](coordinates, ndims)
    }
    if id is not None:
        feature['id'] = id
    return feature


def create_features_from_multi(type, geoms, ids, ndims):
    for o in itertools.izip_longest(geoms, ids):
        yield create_feature(type, o[0], o[1], ndims)


def create_multipoint(geoms, ids, ndims):
    return create_features_from_multi(constants.POINT, geoms, ids, ndims)


def create_multilinestring(geoms, ids, ndims):
    return create_features_from_multi(constants.LINESTRING, geoms, ids, ndims)


def create_multipolygon(geoms, ids, ndims):
    return create_features_from_multi(constants.POLYGON, geoms, ids, ndims)


def create_features_from_collection(geoms, ids, ndims):
    for o in itertools.izip_longest(geoms, ids):
        yield create_feature(o[0]['type'], o[0]['coordinates'], o[1], ndims)


def create_collection(geoms, ids, ndims):
    return create_features_from_collection(geoms, ids, ndims)


transforms = {}
transforms[constants.POINT] = create_point
transforms[constants.LINESTRING] = create_linestring
transforms[constants.POLYGON] = create_polygon
transforms[constants.MULTIPOINT] = create_multipoint
transforms[constants.MULTILINESTRING] = create_multilinestring
transforms[constants.MULTIPOLYGON] = create_multipolygon
transforms[constants.COLLECTION] = create_collection
