# reference: http://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
# test:  http://overpass-turbo.eu/

/* Ways and nodes */
(
  relation(2941631);
  way(r);
  node(w);
);
out meta;
//http://overpass-api.de/api/interpreter?data=%28relation%282941631%29%3Bway%28r%29%3Bnode%28w%29%3B%29%3Bout%20meta%3B%0A


/* Only bus stops */
(
  relation(2941631);
  node["public_transport"="stop_position"](r);
);
out meta;
// http://overpass-api.de/api/interpreter?data=%28relation%282941631%29%3Bnode%5B%22public%5Ftransport%22%3D%22stop%5Fposition%22%5D%28r%29%3B%29%3Bout%20meta%3B%0A


<query type="relation">
  <has-kv k="ref" v="CE 61"/>
</query>
<recurse type="relation-way"/>
<print/>


  wget -O exports/buses/$2.osm "http://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%3B(rel($3)%3Bway(r)%3Bnode(w)%3B)%3Bout%20meta%3B"

  wget -O foo.osm "http://overpass-api.de/api/interpreter?data=%28relation%282941631%29%3Bnode%5B%22public%5Ftransport%22%3D%22stop%5Fposition%22%5D%28r%29%3B%29%3Bout%20meta%3B%0A"




if [ "$1" = "buslines" ]; then
  echo -e "Downloading bus lines form Managua from OpenStreetMap."

  # Loop through csv
  while IFS=, read bus_id relation_1 relation_2
  do

    # Download available relations
    if [ -n "$relation_1" ]; then
      wget -O export/osm/$bus_id.1.route.osm "http://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%3B(rel($relation_1)%3Bway(r)%3Bnode(w)%3B)%3Bout%20meta%3B"
      wget -O export/osm/$bus_id.1.stops.osm "http://overpass-api.de/api/interpreter?data=%28relation%28$relation_1%29%3Bway%28r%29%3Bnode%28w%29%3B%29%3Bout%20meta%3B%0A"
    fi
    if [ -n "$relation_2" ]; then
      wget -O export/osm/$bus_id.2.route.osm "http://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%3B(rel($relation_2)%3Bway(r)%3Bnode(w)%3B)%3Bout%20meta%3B"
      wget -O export/osm/$bus_id.2.stops.osm "http://overpass-api.de/api/interpreter?data=%28relation%28$relation_2%29%3Bway%28r%29%3Bnode%28w%29%3B%29%3Bout%20meta%3B%0A"
    fi
  done < buslines.csv


fi
