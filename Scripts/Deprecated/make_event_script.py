#!/usr/bin/python
import json
from kafka import KafkaConsumer
import time
import re
consumer = KafkaConsumer(bootstrap_servers ='sandbox-hdf.hortonworks.com:6667',
                        auto_offset_reset = 'earliest',
                        consumer_timeout_ms = 1000)
consumer.subscribe(['project_1'])

messages=[]
for message in consumer:
        messages.append(message[6])

messages_1=[]
messages_proxy=[]
for message in messages:
        j = json.loads(message)
        if j['event']['event_id'] not in messages_proxy:
                messages_proxy.append(j['event']['event_id'])
                messages_1.append(j)

print(len(messages),len(messages_proxy),len(messages_1))

with open("/root/meetup_stuffs/test_event.txt", "w") as f:
        i=0
        for message in messages_1:
                i+=1
                message['event']['event_name'] = re.sub('\"*','',message['event']['event_name'])
		f.write('(id_'+str(message['event']['event_id'])+':Event{name:'+'"'+message['event']['event_name'].encode('utf-8')+'"')
		f.write(',event_id:'+'"'+str(message['event']['event_id'])+'"')
		f.write(',event_url:'+'"'+message['event']['event_url'].encode('utf-8')+'"')
		try:
			message['venue']['venue_name'] = re.sub('\"*','',message['venue']['venue_name'])
			f.write(',venue_name:'+'"'+message['venue']['venue_name'].encode('utf-8')+'"')
			f.write(',long:'+'"'+str(message['venue']['lon'])+'"')
			f.write(',lat:'+'"'+str(message['venue']['lat'])+'"')
			f.write(',venue_id:'+'"'+str(message['venue']['venue_id'])+'"}),\n')
		except:
			f.write('}),\n')	
			
			print "\n#######"+str(i)+"#########\n"


                	#except:
                	#       print "########################### \n error occurred \n ####################$
print "got till here, digit \"cat test_event.txt\" to visualize the output file"
