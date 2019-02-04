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
        if j['group']['group_id'] not in messages_proxy:
                messages_proxy.append(j['group']['group_id'])
                count+=1
                print "\n#####"+str(count)+"#####"
		messages_1.append(j['group'])


graph = Graph(password = 'neo4j', host = 'localhost')
#graph.delete_all()

count = 0
for message in messages_1:

                new_node = Node('Group',
                        name = message['group_name'],
                        id = message['group_id'],
                	city = message['group_city'],
			country = message['group_country'],
			long = message['group_lon'],
			lat = message['group_lat'],
			url = message['group_urlname'])
		graph.create(new_node)
                count+=1
                print"##node number\t"+str(count)+"\t just created##"

print(len(messages),len(messages_1),len(messages_proxy))
