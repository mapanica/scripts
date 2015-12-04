# reference: http://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
# test:  http://overpass-turbo.eu/

/* Ways and nodes */
(
  relation(2941631);
  way(r);
  node(w);
);
out meta;


/* Only bus stops */
(
  relation(2941631);
  node["public_transport"="stop_position"](r);
);
out meta;



<query type="relation">
  <has-kv k="ref" v="CE 61"/>
</query>
<recurse type="relation-way"/>
<print/>


  wget -O exports/buses/$2.osm "http://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%3B(rel($3)%3Bway(r)%3Bnode(w)%3B)%3Bout%20meta%3B"

  wget -O foo.osm "http://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%3B(rel(2941631)%3Bway(r)%3Bnode(w)%3B)%3Bout%20meta%3B"
