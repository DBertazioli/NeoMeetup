//headers: event_id,venue_id

return "Importing event-venue relations";

LOAD CSV WITH HEADERS FROM "file:///relations_events-venues.csv" AS row
MATCH (venue:Venue {id: row.venue_id})
MATCH (event:Event {id: row.event_id})
MERGE (event)-[:HOSTED_AT]->(venue);
       
return "Imported event-venue relations";