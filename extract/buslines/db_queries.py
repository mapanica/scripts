#!/usr/bin/python
# -*- coding: utf-8 -*-
import db_connection

# Set up database connection
con = db_connection.get_db()

def get_busline(relation_id):

    # Execute query to obtain line of bus route
    sql = "SELECT ST_LineMerge(ST_Transform(ST_Collect(way), 4326)) FROM planet_osm_line JOIN (SELECT ltrim(member, 'w')::bigint AS osm_id FROM (SELECT unnest(members) AS member FROM  planet_osm_rels WHERE  id = " + str(relation_id) + ") u WHERE member LIKE 'w%') x USING (osm_id)";
    busline = con.ExecuteSQL(sql);
    return busline;

def get_busstops(relation_id):

    # Execute query to obtain points of bus stops
    sql = "SELECT name, public_transport, highway, '' AS official_status, amenity, osm_id, ST_Transform(way, 4326) FROM planet_osm_point JOIN (SELECT ltrim(member, 'n')::bigint AS osm_id FROM (SELECT unnest(members) AS member FROM planet_osm_rels WHERE id = " + str(relation_id) + ") u WHERE member LIKE 'n%') x USING (osm_id) WHERE public_transport = 'platform'";
    busstops = con.ExecuteSQL(sql);
    return busstops;

def get_stoparea(node_id):

    # Execute query to obtain bus stop area relation
    sql = "SELECT id, tags FROM planet_osm_rels WHERE ARRAY['public_transport','stop_area']<@tags AND ARRAY['n" + str(node_id) + "','platform']<@members";
    stoparea = con.ExecuteSQL(sql);
    return stoparea;

def get_routemaster(relation_id):

    # Execute query to obtain route master relation
    sql = "SELECT id, tags FROM planet_osm_rels WHERE ARRAY['type','route_master']<@tags AND ARRAY['r" + str(relation_id) + "', '']<@members";
    routemaster = con.ExecuteSQL(sql);
    return routemaster;

def get_length(relation_id):
    sql = "SELECT ST_Length(ST_Transform(ST_Collect(way), 4326)) FROM planet_osm_line JOIN (SELECT ltrim(member, 'w')::bigint AS osm_id FROM (SELECT unnest(members) AS member FROM  planet_osm_rels WHERE  id =" + str(relation_id) + ") u WHERE member LIKE 'w%') x USING (osm_id)"
    busline_length = con.ExecuteSQL(sql);
    print busline_length.GetNextFeature().st_length*111.195;
    return busline_length;
