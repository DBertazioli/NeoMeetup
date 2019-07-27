#!/usr/bin/python
import json
from kafka import KafkaConsumer
import time
import re
from py2neo import Graph, Node, Path, NodeMatcher, Relationship


consumer = KafkaConsumer(bootstrap_servers ='sandbox-hdf.hortonworks.com:6667',
                        auto_offset_reset = 'earliest',
                        consumer_timeout_ms = 1000)

consumer.subscribe(['project_1'])
count = 0
messages = []
for message in consumer:
        count+=1
        messages.append(message[6])
        if count == 10000:
                break

messages_1=[]
messages_proxy=[]
count = 0

for message in messages:
        j = json.loads(message)
        if j['event']['event_id'] not in messages_proxy:
                messages_proxy.append(j['event']['event_id'])
                count+=1
                print "\n#####"+str(count)+"#####"
		messages_1.append(j)

graph = Graph(password = 'neo4j', host = 'localhost')
graph.delete_all()

count = 0
for message in messages_1:
		try:
                	new_node = Node('Event',
                        	name = message['event']['event_name'],
                        	id = message['event']['event_id'],
                        	time = message['event']['time'],
                        	url = message['event']['event_url'],
				venue_name = ['venue']['venue_name'],
				long = ['venue']['lon'],
				lat = ['venue']['lat'],
				venue_id = ['venue']['id'])
                	graph.create(new_node)
		except:
			new_node = Node('Event',
                                name = message['event']['event_name'],
                                id = message['event']['event_id'],
                                url = message['event']['event_url'])
			graph.create(new_node)
                count+=1
                print"##node number\t"+str(count)+"\t just created##"

print(len(messages),len(messages_1),len(messages_proxy))
