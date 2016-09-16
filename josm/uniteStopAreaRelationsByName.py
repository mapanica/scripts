

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

    relations = dict();
    i = 0;

    print "Start";
    # Loop through all stop area relations
    for relation in mv.editLayer.data.getRelations():

        if (relation.get('public_transport') == 'stop_area'):

            name = relation.get('name');

            if name not in relations.keys():
                relations[name] = relation;

            elif isinstance(name, basestring):

                # Get one node of each relations
                for member in relation.getMembers():
                    if member.isNode():
                        firstNode = member.getNode();

                for member in relations[name].getMembers():
                    if member.isNode():
                        secondNode = member.getNode();

                # Compare distance between nodes from two relations
                distance = firstNode.getCoor().distanceSq(secondNode.getCoor())

                # If they are close enough, we assume to have two stop areas we can merge
                if distance < 0.00003:

                    # Add members from one relation to the other
                    for member in relations[name].getMembers():
                        relation.addMember(member);

                    # Delete the other relation
                    print 'Relation unite! ' + name;
                    DeleteAction.deleteRelation(Main.getLayerManager().getEditLayer(), relations[name]);
                    i = i +1;

    print i;
