return "deleting all topics";

MATCH (t:Topic)
DETACH DELETE t;

return "deleted all topics":
