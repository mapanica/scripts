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

busstops_all = [];
buslines_all = [];

# Run through buslines
for route_relation in con.ExecuteSQL(sql):

    # Get and prepare data on bus line
    route = dict(zip(route_relation.tags[0::2], route_relation.tags[1::2]))
    route['id'] = route['ref'] + "-" + route['direction'];
    route['relation_id'] = route_relation.id;
    route['busline'] = db_queries.get_busline(route_relation.id).GetNextFeature();

    # Store global buslines
    buslines_all.append(route);

    # Get data about stops
    busstops = [];
    busstops_raw = db_queries.get_busstops(route_relation.id);
    busstop = busstops_raw.GetNextFeature();
    stopAttributes = dict();
    while busstop is not None:
        stoparea = db_queries.get_stoparea(busstop.GetField('osm_id'));
        for sa in stoparea:
            stoparea_tags_raw = sa.GetField('tags');
            stoparea_tags = dict(zip(stoparea_tags_raw[0::2], stoparea_tags_raw[1::2]))
            try:
                busstop.SetField('name', stoparea_tags['name']);
            except KeyError:
                busstop.SetField('name', '');

            try:
                busstop.SetField('official_status', stoparea_tags['official_status']);
            except KeyError:
                e = ('No information found about official status on stop area');

        # Store route bus stops
        busstops.append(busstop);

        # Store global bus stops
        busstops_all.append(busstop);

        busstop = busstops_raw.GetNextFeature();

    # Convert to seperate GeoJson files
    #filehandler.write_json(route, busstops);

    # Calculate route lenght
    #busline_length = db_queries.get_length(route_relation);

    # Debugging
    #logging.debug(route['id']);

# Convert global SHP files
filehandler.write_routes_shp(buslines_all);
filehandler.write_stops_shp(busstops_all);
