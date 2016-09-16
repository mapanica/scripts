#!/bin/jython
'''
This code is released under the
WTFPL – Do What the Fuck You Want to Public License.
'''
from javax.swing import JOptionPane
from org.openstreetmap.josm import Main
import org.openstreetmap.josm.command as Command
import org.openstreetmap.josm.data.osm.Node as Node
import org.openstreetmap.josm.data.osm.Way as Way
import org.openstreetmap.josm.data.osm.Relation as Relation
import org.openstreetmap.josm.data.Bounds as Bounds
import org.openstreetmap.josm.data.osm.visitor.BoundingXYVisitor as BoundingXYVisitor
import org.openstreetmap.josm.data.osm.TagCollection as TagCollection
import org.openstreetmap.josm.data.osm.DataSet as DataSet
import org.openstreetmap.josm.data.osm.RelationMember as RelationMember
import org.openstreetmap.josm.actions.search.SearchAction as SearchAction
import org.openstreetmap.josm.actions.mapmode.DeleteAction as DeleteAction
import re, time, sys
import codecs

def getMapView():
    if Main.main and Main.main.map:
        return Main.main.map.mapView
    else:
        return None

mv = getMapView()
if mv and mv.editLayer and mv.editLayer.data:

    names = dict();
    i = 0;

    print "Start";
    # Loop through all stop area relations
    for relation in mv.editLayer.data.getRelations():

        if (relation.get('public_transport') == 'stop_area'):

            name = relation.get('name');

            if name not in names.keys():
                names[name] = name;

            elif isinstance(name, basestring):
                print name;
