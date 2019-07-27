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

with open('/root/NeoMeetup/csv/struttura/relations_members-groups.csv', 'wb') as f:
    f.write("member_id,group_id\n")
    for count, message in enumerate(consumer):
        j = json.loads(message.value)        
        try:
            f.write(str(j['member']['member_id'])+","+str(j['group']['group_id'])+"\n")
        except:
            try:
                f.write(str(j['member']['member_id'])+","+"NONE"+"\n")
            except:
                f.write("NONE"+","+str(j['group']['group_id'])+"\n")
        '''if count==9:
            print "count is "+str(count)
            break'''

time=(time.time()-start_t)/60
print "processed messages: "+str(count+1)
print "completed in "+str(time)+" minutes"