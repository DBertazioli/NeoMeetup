#!/usr/bin/python
import json
import csv
import ast
from pprint import pprint
from kafka import KafkaConsumer
import time
import pandas as pd

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)
consumer.subscribe(['project'])
print("subscribed to topic meetup")
messages = []
topics= {}
start = time.time()
for count, filename in enumerate(consumer):
    try:
        j = json.loads(filename.value)
        group_topics = j['group']['group_topics']
        for topic in group_topics:
            topic_url = topic['urlkey']
            try:
                if topic_url not in topics:
                    topics[topic_url]= ast.literal_eval(json.dumps(topic))
                #groups[group_id].pop("group_id")
            except Exception, ex:
                print("inner for")
                print ex            
    except Exception, e:
        print("out for")
        print e
    #if count == 5:
        #break
end = time.time()        
print "processed messages: "+str(count+1)
print " names dict lenght: "+str(len(topics))+" processed in "+str((end-start)/60)+" minutes"

with open('/root/csv/group_topics.csv', 'wb') as f:  
    fields=["topic_name","urlkey"]
    w = csv.DictWriter(f, fields)
    w.writeheader()
    for k in topics:
        w.writerow({field: topics[k].get(field) or "NONE" for field in fields})
        

print "Try to add topic_index"

df = pd.read_csv("/root/csv/group_topics.csv")
df.sort_values('urlkey', inplace = True)
df = df.reset_index()
df.to_csv("/root/csv/group_topics_indexed.csv", index = True, index_label = "topic_id")

print "Done!"