

#!/bin/jython
'''
This code is released under the
WTFPL – Do What the Fuck You Want to Public License.


#from stop position search for nearest platform in this relation (not too far away)


1 .loop through stop_positions which are not in a stop_area relation, yet.
2. search for the closest platform in a route relation
3. make sure it's not too far away (start small and check)
4. define it's name (from stop_position or platform, store the other one and additional tags)
5. create new relation with both elements, correct roles and the tags

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
            if not (relation.get('name') == None):
                for member in relation.getMembers():
                    if member.isNode():
                        memberPrimitive = member.getNode()
                    elif member.isWay():
                        memberPrimitive = member.getWay()

                    # Get platform
                    if memberPrimitive.get('public_transport') == 'platform':
                        memberPrimitive.put('name', relation.get('name'));
