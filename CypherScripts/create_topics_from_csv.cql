return "Importing topics";

CREATE CONSTRAINT ON (topic:Topic) ASSERT topic.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM "file:///create_topic_nodes_with_names.csv" AS row
WITH DISTINCT row.urlkey AS urlkey, row.topic_name AS name, row.topic_id AS id
MERGE (topic:Topic {id: id})
ON CREATE SET topic.name = name,
              topic.urlkey = urlkey;
       
return "Imported topics";
