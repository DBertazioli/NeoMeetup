#!/usr/bin/env python
# coding: utf-8


import json
import csv
import ast
from pprint import pprint
#from kafka import KafkaConsumer
import time
import pandas as pd
from pandas import DataFrame as df


start_t=time.time()

df = pd.read_csv("../csv/struttura/relations_topics.csv")

df.head(3)


df1= pd.read_csv("../csv/struttura/member_enriched_final.csv")
df1.head(3)

df1=df1.drop(columns='Unnamed: 0')

df1.dropna(inplace=True)

id_list=[]
topic_list=[]
setcount=None
#setcount=1
for count,line  in enumerate(df1.itertuples()):
    topics=df1.topics[line.Index]
    tmp_list=topics.split()
    
    for elem in tmp_list:
        #print(line.Index)
        id_list.append(df1['member_id'][line.Index])
        elem=elem.strip("[").strip("]").strip(",")
        elem=elem.replace("'","")
        topic_list.append(elem)
    if setcount:        
        if count is 2:
            break

            
df2=pd.DataFrame({"type":1,"group_id":"NaN","member_id":id_list,"topic_name":"NaN","urlkey":topic_list})
#print(len(df2))
print df2.head(3)


df['type']=0
df['type']=df['type'].apply(int)

df_c=pd.concat([df, df2], sort=False)
print df_c.head(3)
print df_c.tail(3)


debug=1
if debug:
    print "len(df_c) "+str(len(df_c))
    print "len(df2) "+str(len(df2))
    print "len(df) " +str(len(df))
    print("sum len:"+str(len(df)+len(df2)))

del df
del df1
del df2

df_c.sort_values('urlkey', inplace=True)
#df_c.head()

df_c.reset_index(inplace=True)
df_c.drop('index', axis=1, inplace=True)

df_c['topic_id']=0

temp=df_c.urlkey.at[0]
count=0
index=0

for line in df_c.itertuples():

    curr_url=line.urlkey
    if curr_url == temp:
        df_c['topic_id'].at[line.Index]=count

    else:
        count+=1
        df_c['topic_id'].at[line.Index]=count
        temp=curr_url
    if setcount:
        if count == 20:
            print "breaking"
            break
    
print df_c.head(3)

#df_create_topic=pd.DataFrame([df_c['topic_id'],df_c['urlkey']])
df_create_topic=pd.concat([df_c['topic_id'],df_c['urlkey']], axis=1).reset_index() #eventually add topic_name
print df_create_topic.head(3)
df_create_topic.to_csv("../csv/struttura/Create_topic_nodes.csv", index=False)

del df_create_topic

df_topic_interest=df_c[df_c['type']==0]
df_topic_interest.drop(columns='type', inplace=True)
df_topic_interest.to_csv("../csv/struttura/relations_topics_with_id.csv", index=False)

del df_topic_interest

df_topic_decleared=df_c[df_c['type']==1]
df_topic_decleared.drop(columns=['type','group_id','topic_name'], inplace=True)
df_topic_decleared.to_csv("../csv/struttura/relations_decleared_topics.csv", index=False)


time=(time.time()-start_t)/60
print "completed in "+str(time)+" minutes"

