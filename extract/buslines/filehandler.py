#!/usr/bin/python
# -*- coding: utf-8 -*-

import ogr, osr, os
import db_queries
import logging
import simplejson, json
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def write_json(route, stops):

    # File definitions
    spatialReference = osr.SpatialReference();
    spatialReference.ImportFromProj4('+proj=utm +zone=48N +ellps=WGS84 +datum=WGS84 +units=m');
    driver = ogr.GetDriverByName('GeoJSON');

    # Create file with geo information
    datasource = driver.CreateDataSource(path + route['id'] + ".geojson");
    layer = datasource.CreateLayer(route['id'] + ".geojson", spatialReference, ogr.wkbPoint);
    layer_defn = layer.GetLayerDefn();
    layer.CreateField(ogr.FieldDefn('name', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('attributes'));

    # Adding rute element
    feat = route['busline'].GetNextFeature();
    while feat is not None:

      # Simplifying the data
      foo = feat.GetGeometryRef();
      geometry = ogr.Geometry(ogr.wkbMultiLineString);
      geometry.AddGeometry(foo);

      geometry = geometry.SimplifyPreserveTopology(0.00002);
      # Use only simplified data, if we had an success
      if (geometry.IsEmpty()):
        geometry = foo;

      # Adding data
      featDef = ogr.Feature(layer_defn);
      featDef.SetGeometry(geometry);
      featDef.SetField('name', route['name']);

      # Adding attributes to bus route
      attributes = {'ref': route['ref'], 'to': route['to'], 'from': route['from'], 'network': route['network'], 'operation': route['opening_hours']};
      routemaster = db_queries.get_routemaster(route['relation_id']);
      for rm in routemaster:
          temp_tags = rm.GetField('tags');
          routemaster_tags = dict(zip(temp_tags[0::2], temp_tags[1::2]));
          try:
              attributes['operator'] = routemaster_tags['operator'];
          except KeyError:
              logging.debug('No operator information found on route master')

      featDef.SetField('attributes', simplejson.dumps(attributes));

      # Create file
      layer.CreateFeature(featDef);
      feat.Destroy();
      feat = route['busline'].GetNextFeature();

    for stop in busstops:
      attributes.clear();
      # Adding data
      stopDef = ogr.Feature(layer_defn);
      stopDef.SetGeometry(stop.GetGeometryRef());
      stopDef.SetField('name', stop.GetField('name'));
      try:
          attributes['official_status'] = stop.GetField('official_status');
      except KeyError:
          e = ('No information found about official status on stop area');

      if not (len(attributes) < 0):
          stopDef.SetField('attributes', simplejson.dumps(attributes));

      layer.CreateFeature(stopDef);
      stop.Destroy();
    return;



def write_routes_shp(routes):

    # Define filename input
    path = 'export/shp/';

    # Shape file definitions
    spatialReference = osr.SpatialReference();
    spatialReference.ImportFromProj4('+proj=utm +zone=48N +ellps=WGS84 +datum=WGS84 +units=m');
    driver = ogr.GetDriverByName('ESRI Shapefile');

    # Create shapefile for routes
    shapeData = driver.CreateDataSource(path);
    layer = shapeData.CreateLayer("mapanica-routes", spatialReference, ogr.wkbLineString);
    layer_defn = layer.GetLayerDefn();
    layer.CreateField(ogr.FieldDefn('ref', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('name', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('origin', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('dest', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('first', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('last', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('duration', ogr.OFTString));

    for route in routes:

      # Adding data
      featDef = ogr.Feature(layer_defn);
      featDef.SetGeometry(route['busline'].GetGeometryRef());
      featDef.SetField('ref', route['ref']);
      featDef.SetField('name', route['name']);
      featDef.SetField('origin', route['from']);
      featDef.SetField('dest', route['to']);
      featDef.SetField('first', route['opening_hours']);
      featDef.SetField('last', route['opening_hours']);
      featDef.SetField('duration', route['duration']);

      # Create file
      layer.CreateFeature(featDef);

    return;



def write_stops_shp(stops):

    # Define filename input
    path = 'export/shp/';

    # Shape file definitions
    spatialReference = osr.SpatialReference();
    spatialReference.ImportFromProj4('+proj=utm +zone=48N +ellps=WGS84 +datum=WGS84 +units=m ');
    driver = ogr.GetDriverByName('ESRI Shapefile');

    # Create shapefile for stops
    shapeData = driver.CreateDataSource(path);
    layer = shapeData.CreateLayer("mapanica-stops", spatialReference, ogr.wkbPoint);
    layer_defn = layer.GetLayerDefn();
    layer.CreateField(ogr.FieldDefn('name', ogr.OFTString));

    for stop in stops:

      # Adding data
      featDef = ogr.Feature(layer_defn);
      featDef.SetGeometry(stop.GetGeometryRef());
      featDef.SetField('name', stop.GetField('name'));

      # Create file
      layer.CreateFeature(featDef);

    return;
