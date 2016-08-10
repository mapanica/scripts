#!/usr/bin/python
# -*- coding: utf-8 -*-

import ogr, osr, os
import db_queries
import logging
import simplejson, json


def write_json(relation_id, businfo, busline, busstops):

    busnumber = businfo['ref'];

    # Define filename
    path = 'export/geojson/';
    if os.path.isfile(path + busnumber + "-1" + ".geojson"):
        route_direction = "2";
    else:
        route_direction = "1";

    # File definitions
    spatialReference = osr.SpatialReference(); #will create a spatial reference locally to tell the system what the reference will be
    spatialReference.ImportFromProj4('+proj=utm +zone=48N +ellps=WGS84 +datum=WGS84 +units=m'); #here we define this reference to be utm Zone 48N with wgs84...
    driver = ogr.GetDriverByName('GeoJSON'); # will select the driver foir our shp-file creation.

    # Create file with geo information
    datasource = driver.CreateDataSource(path + busnumber + "-" + route_direction + ".geojson"); #so there we will store our data
    layer = datasource.CreateLayer(busnumber + "-" + route_direction + ".geojson", spatialReference, ogr.wkbPoint); #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn(); # gets parameters of the current shapefile
    layer.CreateField(ogr.FieldDefn('name', ogr.OFTString));
    layer.CreateField(ogr.FieldDefn('attributes'));

    # Adding rute element
    feat = busline.GetNextFeature();
    while feat is not None:

      logging.debug(businfo['name']);

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
      featDef.SetField('name', businfo['name']);

      # Adding attributes to bus route
      attributes = {'ref': businfo['ref'], 'to': businfo['to'], 'from': businfo['from'], 'network': businfo['network']};
      #businfo['opening_hours']);
      routemaster = db_queries.get_routemaster(relation_id);
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
      feat = busline.GetNextFeature();

    for stop in busstops:
      # Adding data
      stopDef = ogr.Feature(layer_defn);
      stopDef.SetGeometry(stop.GetGeometryRef());
      stopDef.SetField('name', stop.GetField('name'));
      layer.CreateFeature(stopDef);
      stop.Destroy();
    return;


def write_shp(busnumber, busline, busstops):

    # Define filename input
    path = 'export/shp/';
    if os.path.isfile(path + busnumber + "-1" + "-stops.shp"):
        route_direction = "2";
    else:
        route_direction = "1";

    # Shape file definitions
    spatialReference = osr.SpatialReference(); #will create a spatial reference locally to tell the system what the reference will be
    spatialReference.ImportFromProj4('+proj=utm +zone=48N +ellps=WGS84 +datum=WGS84 +units=m'); #here we define this reference to be utm Zone 48N with wgs84...
    driver = ogr.GetDriverByName('ESRI Shapefile'); # will select the driver foir our shp-file creation.

    # Create shapefile for stops
    shapeData = driver.CreateDataSource(path); #so there we will store our data
    layer = shapeData.CreateLayer(busnumber + "-" + route_direction + "-stops", spatialReference, ogr.wkbPoint); #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn(); # gets parameters of the current shapefile
    fd = ogr.FieldDefn('name',ogr.OFTString);
    layer.CreateField(fd);

    # Adding elements
    feat = busstops.GetNextFeature();
    while feat is not None:
      featDef = ogr.Feature(layer_defn);
      featDef.SetGeometry(feat.GetGeometryRef());
      featDef.SetField('name',feat.name);
      layer.CreateFeature(featDef);
      feat.Destroy();
      feat = busstops.GetNextFeature();

    # Create shapefile for route
    shapeData = driver.CreateDataSource(path); #so there we will store our data
    layer = shapeData.CreateLayer(busnumber + "-" + route_direction + "-route", spatialReference, ogr.wkbLineString); #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn(); # gets parameters of the current shapefile

    # Adding elements
    feat = busline.GetNextFeature();
    while feat is not None:
      featDef = ogr.Feature(layer_defn);
      featDef.SetGeometry(feat.GetGeometryRef());
      layer.CreateFeature(featDef);
      feat.Destroy();
      feat = busline.GetNextFeature();


    shapeData.Destroy(); #lets close the shapefile
    return;
