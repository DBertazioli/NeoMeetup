#!/usr/bin/python
import json
from kafka import KafkaConsumer
import time

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
			auto_offset_reset = 'earliest',
			consumer_timeout_ms = 1000)
consumer.subscribe(['project_1'])

with open("/root/Meetup/neo_try.txt", "w") as f:
	i=0
	#while True:
	for message in consumer:
		i+=1
		j = json.loads(message.value)
		try:
			f.write("("+str(j['member']['member_id'])+"\t:\tPerson { name\t:\t"+str(j['member']['member_name'])+"}),\n")
			print "\n#######"+str(i)+"#########\n"
		except Exception, e:
			print "########################### \n error occurred \n #######################################"
			print e
			print j['member']['member_name']
		if i==10:
			break
print "got till here, digit \"cat neo_try.txt\" to visualize the output file"
