return "deleting all nodes and relationships";

MATCH (n)
DETACH DELETE n;

return "deleted all nodes and relationships":
