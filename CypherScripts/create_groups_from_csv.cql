//headers: group_id,group_city,group_country,group_lat,group_lon,group_name,group_state,group_topics,group_urlname

return "Importing groups";

CREATE CONSTRAINT ON (group:Group) ASSERT group.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM "file:///group.csv" AS row
WITH DISTINCT row.group_id AS id, row.group_name AS name, row.group_city AS city, row.group_country AS country , row.group_lat AS lat, row.group_lon AS lon, row.group_state AS state, row.group_topics AS topics, row.group_urlname AS urlname

MERGE (group:Group { id:id})
ON CREATE SET group.name = name,
       group.city=city,
       group.country=country,
       group.lat=lat,
       group.lon=lon,
       group.state=state,
       group.topics=topics,
       group.urlname = urlname;
       
return "Imported groups";
