

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

    selectedNodes = mv.editLayer.data.getSelectedNodes()
    platform = Node()

    # Find stop_position nodes
    for platform in selectedNodes:
        if (platform.get('public_transport') == 'platform'):

            print platform.getId()

            # Check if stop position is alrady in a stop area relation
            nodeInRelation = False
            exampleRoute = Relation()
            stop_position = Node()
            distance = 0.00000006

            for parent in platform.getReferrers():
                parentTags = parent.getKeys()

                if (parentTags.get('public_transport') == 'stop_area'):
                    print 'Platform already has a stop area relation'
                    nodeInRelation = True

                # Grab bus route for later
                elif (parentTags.get('type') == 'route'):
                    exampleRoute = parent

            if not nodeInRelation:

                # Get closest stop_position for stop position
                for member in exampleRoute.getMembers():
                    if member.isNode():
                        possibleStop = member.getNode()
                    elif member.isWay():
                        possibleStop = member.getWay()

                    if possibleStop.get('public_transport') == 'stop_position':
                        # Calculate distance to stop position
                        possibleDistance = possibleStop.getCoor().distanceSq(platform.getCoor())
                        if possibleDistance < distance:
                            distance = possibleDistance
                            stop_position = possibleStop

                # Continue only if stop position candidate was found
                if stop_position.getId() > 0:

                    # Create new stop area relation
                    stopArea = Relation()
                    stopArea.addMember(RelationMember('stop', stop_position))
                    stopArea.addMember(RelationMember('platform', platform))


                    # Define tags for relation
                    stopArea.put('type', 'public_transport')
                    stopArea.put('public_transport', 'stop_area')
                    stopArea.put('public_transport:version', '2')
                    platformTags = platform.getInterestingTags()
                    stopPositionTags = stop_position.getInterestingTags()
                    if platformTags.get('name'):
                        stopArea.put('name', platformTags.get('name'))
                        if stopPositionTags.get('name'):
                            stopArea.put('alt_name', stopPositionTags.get('name'))
                    elif stopPositionTags.get('name'):
                        stopArea.put('name', stopPositionTags.get('name'))

                    if platformTags.get('official_name'):
                        stopArea.put('official_name', platformTags.get('official_name'))
                        if stopPositionTags.get('official_name'):
                            stopArea.put('alt_official_name', stopPositionTags.get('official_name'))
                    elif stopPositionTags.get('official_name'):
                        stopArea.put('official_name', stopPositionTags.get('official_name'))

                    # Write newly created stop area relation to data layer
                    print stopArea.get('name')
                    mv.editLayer.data.addPrimitive(stopArea)

                else:
                    print 'No stop position candidate found'
            else:
                print 'No platform found in selection'
