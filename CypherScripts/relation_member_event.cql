//headers: member_id,event_id,response

return "Importing member-event relations";

USING PERIODIC COMMIT 50000

LOAD CSV WITH HEADERS FROM "file:///relations_member-event-response_new.csv" AS row
MATCH (member:Member {id: row.member_id})
MATCH (event:Event {id: row.event_id})
MERGE (member)-[:WILL_PARTECIPATES {response: row.response, guests: row.guests}]->(event);
       
return "Imported member-event-response relations";
