#!/usr/bin/python
import json
import time
from kafka import KafkaConsumer

start_t=time.time()

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)

consumer.subscribe(['project_april'])
print("subscribed to topic project")

with open('/root/NeoMeetup/csv/struttura/relations_groups-events.csv', 'wb') as f:
    f.write("group_id,event_id\n")
    for count, message in enumerate(consumer):
        j = json.loads(message.value)        
        try:
            f.write(str(j['group']['group_id'])+","+str(j['event']['event_id'])+"\n")
        except:
            try:
                f.write(str(j['group']['group_id'])+","+"NONE"+"\n")
            except:
                f.write("NONE"+","+str(j['event']['event_id'])+"\n")
        '''if count==90:
            print "count is "+str(count)
            break'''

print"already wrote "+str(count+1)

time=(time.time()-start_t)/60
print "completed in "+str(time)+" minutes"