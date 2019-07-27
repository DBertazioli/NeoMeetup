//headers: group_id,event_id

return "Importing group-event relations";

USING PERIODIC COMMIT 50000

LOAD CSV WITH HEADERS FROM "file:///relations_groups-events.csv" AS row

MATCH (group:Group {id: row.group_id})
MATCH (event:Event {id: row.event_id})
MERGE (group)-[:HOSTED_EVENT]->(event);
       
return "Imported group-event relations";
