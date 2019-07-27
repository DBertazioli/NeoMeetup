#!/usr/bin/python
import json
from kafka import KafkaConsumer
import pandas as pd
from pandas import DataFrame as df
import time

consumer = KafkaConsumer(bootstrap_servers = 'sandbox-hdf.hortonworks.com:6667',
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)

consumer.subscribe(['project'])
print("subscribed to topic project")

d = []
start = time.time()
for count, message in enumerate(consumer):
    j = json.loads(message.value)        
    try:
        if j['guests']:
            d.append({'member_id':str(j['member']['member_id']),'event_id':str(j['event']['event_id']),
                             'response':str(j['response']),'mtime':str(j['mtime']),'guests':str(j['guests'])})
        else:
            d.append({'member_id':str(j['member']['member_id']),'event_id':str(j['event']['event_id']),
                             'response':str(j['response']),'mtime':str(j['mtime']), 'guests': str(0)})
    except: 
        print '******Errore*****'
        break
    '''if count==100000:
        print "count is "+str(count)
        break'''

df = pd.DataFrame(d)

end = time.time()

print"already wrote "+str(count)+" in "+str(end-start)
print"Time to work on this dataframe!"

start = time.time()

df['id'] = df['member_id'].astype(str) + df['event_id'].astype(str)
df_sorted = df.sort_values("mtime", ascending = False)
df_cleaned = df.drop_duplicates(subset = 'id', keep = 'first')
df_cleaned = df_cleaned.drop(['id', 'mtime'], axis = 1)

end = time.time()

print "Cleaned dataframe has "+str(len(df_cleaned)-1)+" rows, from an initial dataframe of "+str(len(df_sorted)-1)+" rows"
print "This cleaning work required "+str(end-start)

df_cleaned.to_csv("/root/csv/relations_member-event-response[new].csv", index = False)