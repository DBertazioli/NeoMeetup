#!/usr/bin/python
import json
from kafka import KafkaConsumer
import time

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)

consumer.subscribe(['project'])
print("subscribed to topic project")

start = time.time()
count=0
with open('/root/meetup_stuffs/csv/relations.csv', 'wb') as f:
    f.write("member_id,group_id,event_id,venue_id,response\n")
    for message in consumer:
        j = json.loads(message.value)
        count+=1
        try:
            f.write(str(j['member']['member_id'])+","+str(j['group']['group_id'])+","+str(j['event']['event_id'])+","+
                    str(j['venue']['venue_id'])+","+str(j['response'])+"\n")
        except:
            f.write(str(j['member']['member_id'])+","+str(j['group']['group_id'])+","+str(j['event']['event_id'])+","+
                    "NONE"+","+str(j['response'])+"\n")
end = time.time()
print"already wrote "+str(count)+" messages in "+str(end-start)