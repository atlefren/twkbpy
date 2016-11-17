# -*- coding: utf-8 -*-
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

transforms = {}
transforms[constants.POINT] = create_point
transforms[constants.LINESTRING] = create_linestring
transforms[constants.POLYGON] = create_polygon
