#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

def convert_geojson(relation_tags, busline, busstops):
    print busline;
    featurecollection = {
        "type": "FeatureCollection",
        "features": (
            {
              "type": "Feature",
              "properties": {
                "name": relation_tags['ref'],
              },
              "geometry": json.loads(busline[0]),
            },
        ),
    }

    index = 0
    for busstop in busstops:
        if index <= 99:
            featurecollection['features'] = featurecollection['features'] + (
            {
                "type": "Feature",
                "properties": {
                    "name": busstop[0],
                    "popupContent": "This is where the Rockies play!"

                 },
                "geometry": json.loads(busstop[5]),
            },
            )
            index = index + 1

    return json.dumps(featurecollection)
