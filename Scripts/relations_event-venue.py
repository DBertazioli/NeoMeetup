#!/usr/bin/python
import json
import time
from kafka import KafkaConsumer

start_t=time.time()

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 3000)

consumer.subscribe(['project_april'])
print("subscribed to topic project")

with open('/root/NeoMeetup/csv/struttura/relations_events-venues.csv', 'wb') as f:
    f.write("event_id,venue_id\n")
    for count, message in enumerate(consumer):
        j = json.loads(message.value)        
        try:
            f.write(str(j['event']['event_id'])+","+str(j['venue']['venue_id'])+"\n")
        except:
            try:
                f.write(str(j['event']['event_id'])+","+"NONE"+"\n")
            except:
                f.write("NONE"+","+str(j['venue']['venue_id'])+"\n")
        '''if count==90:
            print "count is "+str(count)
            break'''

print "processed messages: "+str(count+1)
time=(time.time()-start_t)/60
print "completed in "+str(time)+" minutes"