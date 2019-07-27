//headers: venue_id,venue_name,lat,lon
return "Importing venues";

CREATE CONSTRAINT ON (venue:Venue) ASSERT venue.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM "file:///venue.csv" AS row
WITH DISTINCT row.venue_id AS id, row.venue_name AS name, row.lat AS lat, row.lon AS lon 
MERGE (venue:Venue {id: id})
ON CREATE SET venue.name = name,
              //venue.city = row.city,
              //venue.address1 = row.address_1,
              //venue.address2 = row.address_2,
              venue.lat = tofloat(lat),
              venue.lon = tofloat(lon);
       
return "Imported venues";
