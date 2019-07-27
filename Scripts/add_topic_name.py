#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_csv("../csv/struttura/create_topic_nodes.csv")


# In[5]:


df.head()


# In[8]:


df['topic_name']="ToBeCreated"


# In[9]:


df.head()


# In[21]:


for count, line in enumerate(df.itertuples()):
    df['topic_name'].at[line.Index]=df['urlkey'].at[line.Index].replace("-", " ")
    #if count is 100:
    #    break
print df.head()


# In[20]:


#print df.topic_name
print df.topic_name.head()
print df.topic_name.tail()

df.to_csv("../csv/struttura/create_topic_nodes_with_names.csv")

# In[ ]:



