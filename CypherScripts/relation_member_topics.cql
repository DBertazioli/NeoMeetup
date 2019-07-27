//headers: member_id,group_id,urlkey,topic_name

return "Importing member-topics relations";

USING PERIODIC COMMIT 50000

LOAD CSV WITH HEADERS FROM "file:///relations_topic_with_id.csv" AS row

MATCH (member:Member {id: row.member_id}), (topic:Topic {id: row.topic_id})
MERGE (member)-[:IS_INTERESTED_IN]->(topic);
       
return "Imported member-topics relations";
