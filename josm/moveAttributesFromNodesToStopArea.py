

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
import re, time, sys
import codecs

def getMapView():
    if Main.main and Main.main.map:
        return Main.main.map.mapView
    else:
        return None

workingTag = 'official_status';
mv = getMapView()
if mv and mv.editLayer and mv.editLayer.data:

    # Loop through all stop area relations
    for relation in mv.editLayer.data.getRelations():

        platformData = None;
        stopPositionData = None;
        stopAreaData = None;
        finalData = None;

        if (relation.get('public_transport') == 'stop_area'):

            #print relation.getId()

            # If stop area alreay has a value
            if not (relation.get(workingTag) == None):
                i = '';
                # print "STOP AREA: " + relation.get(workingTag);

            # Otherwise look for information in members
            else:
                for member in relation.getMembers():
                    if member.isNode():
                        memberPrimitive = member.getNode()
                    elif member.isWay():
                        memberPrimitive = member.getWay()

                    # Get tags to check from stop position
                    if memberPrimitive.get('public_transport') == 'stop_position':
                        stopPositionData = memberPrimitive.get(workingTag);

                    # Get tags to check from platform
                    if memberPrimitive.get('public_transport') == 'platform':
                        platformData = memberPrimitive.get(workingTag);



                ## Check for unexpected tags
                if not (platformData == None) and not (platformData == 'IRTRAMMA:bus_stop') and not (platformData == 'IRTRAMMA:bus_station') and not (platformData == 'none'):
                    print "UNEXSPECTED TAG on Platform: " + platformData;

                if not (stopPositionData == None) and not (stopPositionData == 'IRTRAMMA:bus_stop') and not (stopPositionData == 'IRTRAMMA:bus_station') and not (stopPositionData == 'none'):
                    print "UNEXSPECTED TAG on stopPositionData;


                ## DECIDE

                # Both are fine, so save.
                if (platformData == stopPositionData):
                    if not (platformData == None) and not (stopPositionData == None):
                        finalData = stopPositionData;
                    elif (platformData == None) and (stopPositionData == None):
                        finalData = 'unset';

                # Only one data part exists, so save this one
                elif (platformData == None) and not (stopPositionData == None):
                        finalData = stopPositionData;

                elif (stopPositionData == None) and not (platformData == None):
                        finalData = platformData;

                # At very last trust the platform over the stop_position
                else:
                    finalData = platformData;


                ## STORE
                if (stopAreaData == None) and not (finalData == None):
                    relation.put(workingTag, finalData);
                    print "FILLED: " + finalData;
                else:
                    if (stopPositionData == None):
                        stopPositionData = 'NONE';
                    if (platformData == None):
                        platformData = 'NONE';
                    print "NOT TOUCHED: (S) " + stopPositionData + " (P) " + platformData;
