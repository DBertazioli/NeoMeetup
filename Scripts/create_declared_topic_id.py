#!/usr/bin/python
import json
import csv
import ast
from pprint import pprint
#from kafka import KafkaConsumer
import time
import pandas as pd
from pandas import DataFrame as df


# In[2]:
start_t=time.time()

df = pd.read_csv("Csv/relations_topics.csv")


# In[3]:


#df.head()


# In[4]:


df.sort_values('urlkey', inplace=True)
#df.head()


# In[5]:


df.reset_index(inplace=True)
#df.head()


# In[6]:


df.drop('index', axis=1, inplace=True)


# In[7]:



df['topic_id']=0

temp=df.urlkey.at[0]
count=0
index=0


# In[8]:


for line in df.itertuples():

    curr_url=line.urlkey
    if curr_url == temp:
        df['topic_id'].at[line.Index]=count

    else:
        count+=1
        df['topic_id'].at[line.Index]=count
        temp=curr_url
    #if count == 20:
    #    break
    


# In[9]:


df.head(50)


# In[10]:

time=time.time()-start_t
print "completed in "+str(time)

df.to_csv("relations_topic_with_id.csv")

