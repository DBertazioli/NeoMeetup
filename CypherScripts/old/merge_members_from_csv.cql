return "Importing members";

CREATE INDEX ON :Member(id);
CREATE INDEX ON :Member(name);

LOAD CSV WITH HEADERS FROM "file:///member.csv" AS row
WITH DISTINCT row.member_id AS id, row.member_name AS name
MERGE (member:Member {id: id})
ON CREATE SET member.name = name;
       
return "finished import";
