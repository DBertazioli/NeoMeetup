#!/usr/bin/python
import json
import csv
import ast
import re
import time
from pprint import pprint
from kafka import KafkaConsumer

start_t=time.time()

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)
consumer.subscribe(['project_april'])
print("subscribed to topic meetup")
events= {}
for count, filename in enumerate(consumer):
    try:
        j = json.loads(filename.value)
        j['event']['event_name'] = re.sub('\"*\'*','',j['event']['event_name'])
        event_id = j['event']['event_id']
        try:
            if event_id not in events:
                events[event_id]= ast.literal_eval(json.dumps(j['event']))           
        except Exception, ex:
       			print("inner for")
       			print ex
    except Exception, e:
       		print("outer for")
       		print e

    '''if count==9:
        print "count is "+str(count)
        break'''
          
#pprint(events)
print "################"
print "processed messages: "+str(count+1)
print " names dict lenght: "+str(len(events))

with open('/root/NeoMeetup/csv/struttura/event.csv', 'wb') as f:  
	fields=["event_id","event_name","event_url","time"]
	w = csv.DictWriter(f, fields)
	w.writeheader()
	for k in events:
		w.writerow({field: events[k].get(field) or "NONE" for field in fields})
        
time=(time.time()-start_t)/60
print "completed in "+str(time)+" minutes"