#!/usr/bin/python
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)

consumer.subscribe(['project'])
print("subscribed to topic project")

with open('/root/meetup_stuffs/relations_members-events-response.csv', 'wb') as f:
    f.write("member_id,event_id,response,mtime\n")
    for count, message in enumerate(consumer):
        j = json.loads(message.value)        
        try:
            f.write(str(j['member']['member_id'])+","+str(j['event']['event_id'])+","+str(j['response'])+","+str(j['mtime'])+"\n")
        except: 
            print '******Errore*****'
            break
        '''if count==100000:
            print "count is "+str(count)
            break'''

print"already wrote "+str(count)