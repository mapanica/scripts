#!/usr/bin/python
# -*- coding: utf-8 -*-

# External lib
import sys

# Internal scripts
import db_connection
import db_queries
import conversions
import filehandler


import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up database connection
con = db_connection.get_db()

# Execute query to obtain relations of the lines of the bus network
sql = """SELECT id, tags FROM planet_osm_rels WHERE ARRAY['type','route']<@tags AND ARRAY['public_transport:version','2']<@tags;""";

# Run through buslines
for route_relation in con.ExecuteSQL(sql):

    # Prepare relation data from db results
    routevariant = route_relation.id;
    routevariant_tags = dict(zip(route_relation.tags[0::2], route_relation.tags[1::2]))

    # Get data
    busline = db_queries.get_busline(routevariant);
    busstops_raw = db_queries.get_busstops(routevariant);
    busstops = [];

    # Get data about stop areas
    busstop = busstops_raw.GetNextFeature();
    while busstop is not None:
        stoparea = db_queries.get_stoparea(busstop.GetField('osm_id'));
        for sa in stoparea:
            stoparea_tags = sa.GetField('tags');
            busstop.SetField('name', stoparea_tags[1]);
        busstops.append(busstop);
        busstop = busstops_raw.GetNextFeature();


    #busline_length = db_queries.get_length(route_relation);
    logging.debug(routevariant_tags);

    # Convert to GeoJson file
    #geojson = conversions.convert_geojson(relation_tags, busline, busstops);


    filehandler.write_json(routevariant, routevariant_tags, busline, busstops);

    # Convert to SHP file
    #filehandler.write_shp(relation_tags['ref'], busline, busstops);

    # Debugging
    #logging.debug(relation_tags['ref'], '%s');
