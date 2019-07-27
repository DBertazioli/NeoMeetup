#!/usr/bin/python
import json 
from kafka import KafkaConsumer 
import time 
import re
consumer = KafkaConsumer(bootstrap_servers ='sandbox-hdf.hortonworks.com:6667',
                        auto_offset_reset = 'earliest',
                        consumer_timeout_ms = 1000) 
consumer.subscribe(['project_1']) 
''' 
messages = [] 
#inizializzo lista
while True:
	for message in consumer:
                print(message[6])
                messages.append(message[6])
        time.sleep(5) j = json.loads(messages[1]) #formatto il singolo messaggio di kafka in json print 
j['value'] #mi restituisce il contenuto di value print j['value']['lat'] #mi restituisce il valore di lat 
all'interno di value
                        #Cos tutto funziona ma appunto abbiamo solo un elemento convertito
''' 
'''
with open("/root/meetup_stuffs/test_neo.txt", "w") as f:
        i=0
	#while True:
        for message in consumer:
                i+=1
                j = json.loads(message.value)
                #try:
                     	#print j['venue']
                        #print "\n"		j['member']['member_name'] = re.sub('\"*','',j['member']['member_name'])
                if j['member']['member_id'] not in f:
		#str_buff=j['member']['member_id']
                f.write("("+"id_"+str(j['member']['member_id']))
                #f.write(str(str_buff))
                f.write(":Person { name:")
                f.write('"'+j['member']['member_name'].encode('utf-8')+'"')
		f.write(",name_id:")
		f.write('"'+str(j['member']['member_id'])+'"')
                f.write("}),\n")
                print "\n#######"+str(i)+"#########\n"
                
                        
                #except:
                #	print "########################### \n error occurred \n ####################$
print "got till here, digit \"cat test_neo.txt\" to visualize the output file"
'''
messages = []		
for message in consumer:
	messages.append(message[6])

messages_1=[]
messages_proxy=[]
for message in messages:
	j = json.loads(message)
	if j['member']['member_id'] not in messages_proxy:
		messages_proxy.append(j['member']['member_id'])
		messages_1.append(j['member'])


print(len(messages),len(messages_1),len(messages_proxy))
print(messages_1[1])

with open("/root/meetup_stuffs/test_member.txt", "w") as f:        
	i=0
        #while True:
        for message in messages_1:
                i+=1
                               #try:
                        #print j['venue']
                        #print "\n"
                message['member_name'] = re.sub('\"*','',message['member_name'])
                #str_buff=j['member']['member_id']
               	f.write("("+"id_"+str(message['member_id']))
               	#f.write(str(str_buff))
               	f.write(":Person { name:")
               	f.write('"'+message['member_name'].encode('utf-8')+'"')
               	f.write(",name_id:")
		f.write('"'+str(message['member_id'])+'"')
               	f.write("}),\n")
               	print "\n#######"+str(i)+"#########\n"


               	#except:
               	#       print "########################### \n error occurred \n ####################$
print "got till here, digit \"cat test_neo.txt\" to visualize the output file"

