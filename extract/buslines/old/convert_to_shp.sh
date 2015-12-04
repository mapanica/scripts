#!/bin/bash
#
# Convert bus lines from osm to shp
#
# felix (ät) delattre (punkt) de
#

# Loop through csv
while IFS=, read bus_id relation_1 relation_2
do
  echo "$bus_id"
  # Convert to geojson
  if [ -n "$relation_1" ]; then
    [[ -d export/shp/$bus_id.1 ]] || mkdir export/shp/$bus_id.1
    osmexport convert/convert_to_shp.oxr export/osm/$bus_id.1.route.osm export/shp/$bus_id.1
  fi
  if [ -n "$relation_2" ]; then
   [[ -d export/shp/$bus_id.2 ]] || mkdir export/shp/$bus_id.2
   osmexport convert/convert_to_shp.oxr export/osm/$bus_id.2.route.osm export/shp/$bus_id.2
  fi
done < buslines.csv
