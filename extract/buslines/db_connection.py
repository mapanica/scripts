import ogr

con = None

def connect():
    global con

    con = ogr.Open("PG: host=localhost dbname=osm_managua user=postgres")
    if con is None:
      print 'Could not open a database or GDAL is not correctly installed!'

def get_db():
    if not (con):
        connect()
    return (con)
