#!/usr/bin/python
import json
import csv
from kafka import KafkaConsumer
import time
import pandas as pd
from pandas import DataFrame as df

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 3000)
consumer.subscribe(['project_april'])
print "subscribed to topic meetup"
d = []
count = 0
start = time.time()
with open("/root/NeoMeetup/csv/struttura/relations_topics.csv", "wb") as csv:
    csv.write("group_id,member_id,topic_name,urlkey"+"\n")
    for message in consumer:
        count +=1
        try:
            j = json.loads(message.value)
            group_topics = j['group']['group_topics']
            for topic in group_topics:
                try:
                    csv.write(str(j['group']['group_id'])+","+str(j['member']['member_id'])+",\""+
                             str(topic['topic_name'].encode('utf-8'))+"\","+str(topic['urlkey'].encode('utf-8'))+"\n")
                except Exception as e: 
                    print e
                    break
        except Exception as ex: 
            print ex
            break
        '''if count==100000:
            print "count is "+str(count)
            break'''
end = time.time()
print "list created in "+str((end-start)/60)+" minutes"
print "Processed "+str(count)+" messages"
