
return "Enriching members with lat-long";

USING PERIODIC COMMIT 50000

LOAD CSV WITH HEADERS FROM "file:///member_enriched_final.csv" AS row

MATCH (member:Member {id: row.member_id})
SET member.lat = row.lat,
       member.long = row.long;
       
return "Enriched members with lat-long";