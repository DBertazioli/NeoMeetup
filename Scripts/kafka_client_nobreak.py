#!/usr/bin/python
import json
import sys
from kafka import KafkaConsumer
import time

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
			auto_offset_reset = 'earliest',
			consumer_timeout_ms = 1000)
consumer.subscribe(['project_1'])

with open("/root/Meetup/neo_try.txt", "w") as f:
	#i=0
	#while True:
	for message in consumer:
		#i+=1
		#print type(message)
		j = json.loads(message.value)
		
#		print type(j)
#		j = {k: unicode(v).decode("utf-8") for k,v in js.iteritems()}
#		j.encode('latin-1).decode('utf-8')
#		print j['member']['member_id'] + "\n"
#		print j['member']['member_name'] + "\n"
		try:
#			f.write("("+str(j['member']['member_id']).decode('latin-1')encode('utf-8')+"\t:\tPerson { name\t:\t"+str(j['member']['member_name']).decode('latin-1').encode('utf-8')+"}),\n")
#			f.write("("+str(j['member']['member_id'])+"\t:\tPerson { name\t:\t"+str(j['member']['member_name'])+"}),\n")
			f.write("("+str(j['member']['member_id']).encode('utf-8')+"\t:\tPerson { name\t:\t"+j['member']['member_name'].encode('utf-8')+"}),\n")
			#print "\n#######"+str(i)+"#########\n"
		except Exception, e:
			print "########################### \n error occurred \n #######################################"
			print e
#			print j['member']['member_name']
		#if i==10:
		#	break
print "got till here, digit \"cat neo_try.txt\" to visualize the output file"
