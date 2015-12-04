#!/usr/bin/python
# -*- coding: utf-8 -*-



colnames = [desc[0] for desc in cur.description]

# Initialize CSV export
ofile  = open('export/csv/' + bus_line_ref + '.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# Write header line
writer.writerow(colnames)
# Export rows
for bus_stop in bus_stops:
  writer.writerow(bus_stop)

ofile.close

