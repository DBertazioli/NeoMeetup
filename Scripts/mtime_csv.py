#!/usr/bin/python
import json
from kafka import KafkaConsumer
import time

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)

consumer.subscribe(['project_april'])
print("subscribed to topic project")

start = time.time()
with open('/root/meetup_stuffs/mtime.csv', 'wb') as f:
    f.write("mtime,group_country,group_state,long,lat\n")
    for count, message in enumerate(consumer):
        j = json.loads(message.value)        
        try:
            f.write(str(j['mtime'])+","+str(j['group']['group_country'])+","+str(j['group']['group_state'])+","+
                    str(j['group']['group_lon'])+","+str(j['group']['group_lat'])+"\n")
        except: 
            f.write(str(j['mtime'])+","+str(j['group']['group_country'])+","+"NONE"+","+
                    str(j['group']['group_lon'])+","+str(j['group']['group_lat'])+"\n")
end = time.time()
print"already wrote "+str(count)+" in "+str((end-start)/60)+" minutes"