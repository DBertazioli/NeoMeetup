//headers: member_id,group_id,urlkey,topic_name

return "Importing group-topics relations";

USING PERIODIC COMMIT 50000

LOAD CSV WITH HEADERS FROM "file:///relations_topic_with_id.csv" AS row

MATCH (group:Group {id: row.group_id}),(topic:Topic {id: row.topic_id})
MERGE (group)-[:DEALS_WITH]->(topic);
       
return "Imported group-topics relations";
