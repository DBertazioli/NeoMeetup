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
        if j['group']['group_id'] not in messages_proxy:
                messages_proxy.append(j['group']['group_id'])
                messages_1.append(j['group'])


print(len(messages),len(messages_1),len(messages_proxy))
print(messages_1[1])

with open("/root/meetup_stuffs/test_group.txt", "w") as f:
        i=0
        for message in messages_1:
        	i+=1
		message['group_name'] = re.sub('\"*','',message['group_name'])
		f.write('(id_'+str(message['group_id'])+':Group{name:'+'"'+message['group_name'].encode('utf-8')+'"'+',id:'+'"'+str(message['group_id'])+'"')
		f.write(',urlname:'+'"'+message['group_urlname'].encode('utf-8')+'"'+',city:'+'"'+message['group_city'].encode('utf-8')+'"'+',country:'+'"'+message['group_country'].encode('utf-8')+'"')
		f.write(',long:'+'"'+str(message['group_lon'])+'"'+',lat:'+'"'+str(message['group_lat'])+'"}),\n')
		print "\n#######"+str(i)+"#########\n"


                #except:
                #       print "########################### \n error occurred \n ####################$
print "got till here, digit \"cat test_group.txt\" to visualize the output file"
