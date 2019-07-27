#!/usr/bin/python
from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)
consumer.subscribe(['project_april'])
print("subscribed to topic meetup")

for count, message in enumerate(consumer):
    pass


print "processed messages: "+str(count)
