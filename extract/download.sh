#!/bin/bash
#
# Script to download Managua bus routes (IRTRAMMA network) from OpenStreetMap
#
# felix (ät) delattre (punkt) de
#

# Ensure valid input.
if [ "$1" != "managua" ]; then
  echo -e "Please specify 'managua'."
  exit
fi

if [ "$1" = "managua" ]; then
  echo -e "Downloading basic OSM map for Managua from OpenStreetMap"
  wget -O export/managua.osm --post-file=definitions/managua-overpass-query.ql "http://overpass-api.de/api/interpreter"
fi

exit

