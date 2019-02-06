#!/usr/bin/python
import json
import csv
from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)
consumer.subscribe(['project'])
print("subscribed to topic meetup")
messages = []
names = {}
for count, message in enumerate(consumer):
    try:        
        #print message.value
        j = json.loads(message.value)
        name_id = j['member']['member_id']
        member_name=j['member']['member_name']
        #print member_name
        try:
            if name_id not in names:
                #messages.append(message[6])
                names[name_id]=member_name.encode('utf-8')                
        except Exception, ex:
            print("inner for")
            print ex
    except Exception, e:
        print("outer for")
        print e

    '''if count==100:
        print "count is "+str(count)
        break'''         
#print names
print "################"
print "processed messages: "+str(count)
print " names dict lenght: "+str(len(names))

with open("/root/meetup_stuffs/member.csv", 'wb') as f: 
    w = csv.writer(f)
    w.writerow(['member_id','member_name'])
    w.writerows(names.items())
    