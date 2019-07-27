//headers: member_id,group_id

return "Importing member-group relations";

USING PERIODIC COMMIT 50000

LOAD CSV WITH HEADERS FROM "file:///relations_members-groups.csv" AS row
MATCH (member:Member {id: row.member_id})
MATCH (group:Group {id: row.group_id})
MERGE (member)-[:MEMBER_OF]->(group);
       
return "Imported member-group relations";
