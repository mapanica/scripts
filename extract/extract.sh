#!/bin/bash
#
# Script to extract Managua bus routes (IRTRAMMA network) from OpenStreetMap
# and convert it to various suitable formats.
#
# felix (ät) delattre (punkt) de
#

echo ""
echo "EXTRACT MANAGUA PUBLIC TRANSPORT INFO SCRIPT"
echo ""

# Download data from OSM
./download.sh managua

# Prepare postgres database
./postgis.sh

# Remove old data
rm -rf export/geojson/*
rm -rf export/shp/*


# Extract seperate osm xml files for each route
python buslines/export_buslines.py

echo "--- done  ---"
exit
