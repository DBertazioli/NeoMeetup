#!/usr/bin/python
import json
import csv
import ast
import time
from pprint import pprint
from kafka import KafkaConsumer

start_t=time.time()

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)
consumer.subscribe(['project_april'])
print("subscribed to topic meetup")
venues= {}
e_o=0
e_i=0
for count, filename in enumerate(consumer):
    try:
        j = json.loads(filename.value)
        venue_id = j['venue']['venue_id']
        try:
            if venue_id not in venues:
                venues[venue_id]= ast.literal_eval(json.dumps(j['venue']))           
        except Exception, ex:
            e_i+=1
       			#print("inner for")
       			#print ex
    except Exception, e:
        e_o += 1
       		#print("outer for")
       		#print e

    '''if count==100:
        print "count is "+str(count)
        break'''
print 'inner for ' +str(e_i)
print 'outer for ' +str(e_o)
#pprint(venues)
print "################"
print "processed messages: "+str(count+1)
print " names dict lenght: "+str(len(venues))

with open('/root/NeoMeetup/csv/struttura/venue.csv', 'wb') as f:  
	fields=["venue_id","venue_name","lat","lon"]
	w = csv.DictWriter(f, fields)
	w.writeheader()
	for k in venues:
		w.writerow({field: venues[k].get(field) or "NONE" for field in fields})

time=(time.time()-start_t)/60
print "completed in "+str(time)+" minutes"