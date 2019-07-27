return "Importing members";

CREATE CONSTRAINT ON (member:Member) ASSERT member.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM "file:///member.csv" AS row
WITH DISTINCT row.member_id AS id, row.member_name AS name
create (member:Member {id: id, name:name});
       
return "finished import";
