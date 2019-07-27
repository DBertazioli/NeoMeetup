//headers: event_id,event_name,event_url,time

return "Importing events";

CREATE CONSTRAINT ON (event:Event) ASSERT event.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM "file:///event.csv" AS row
WITH DISTINCT row.event_id as id, row.event_name as name, row.event_url as url, row.time as time
MERGE (event:Event {id: id})
ON CREATE SET event.name = name,
              event.time = toint(time),
              event.url = url;
       
return "Imported events";
