
/* Roads of a wider range */
(
  .a;
  way[highway](12,-86.45,15.33,-86.07);
  node(w)->.x;
  rel(bw);
);
out meta;

/* All information about Managua */
(
  .b;
  node(12.058838,-86.374855,12.185720,-86.145515);
  <;
);
out meta;

/* Explicitly the bus routes */
(
  .c;
  relation
    [route=bus]
    [network=IRTRAMMA]
    (12.058838,-86.374855,12.185720,-86.145515);
  way(r);
  node(w);
);
out meta;

/* Water and parks of a wider range */
(
  .d;
  (way[natural=water](12.058838,-86.374855,12.285720,-86.145515);>;);
  (way[natural=scrub](12.058838,-86.374855,12.285720,-86.145515);
  >;);
  (way[natural=wood](12.058838,-86.374855,12.285720,-86.145515);
  >;);
  (way[boundary=national_park](12.058838,-86.374855,12.285720,-86.145515);>;);
 );
out meta;
