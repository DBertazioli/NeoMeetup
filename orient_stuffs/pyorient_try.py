#!/usr/bin/env python
# coding: utf-8

# In[7]:


from __future__ import print_function

import pandas as pd
import subprocess
import time

try:
    import pyorient
except ImportError as e:
    #process = subprocess.Popen("pip install --user pyorient".split(), stdout=subprocess.PIPE)
    process = subprocess.Popen("pip install git+https://github.com/DBertazioli/pyorient --user".split(), stdout=subprocess.PIPE)

    output, error = process.communicate()
    print(output, "error = {}".format(error), e)
    import pyorient


# In[10]:


db="neomeetup1"
my_auth="root"
#local=True #set to false for vm use
local=False
if local:
    addr= "10.9.13.4"
else:
    addr= "localhost"


# In[11]:


client = pyorient.OrientDB(addr, 7687)
session_id = client.connect(my_auth,my_auth)


# In[12]:


#useful funct
def reset_db(client, name):

    # Remove Old Database
    client.db_drop(name)

    # Create New Database
    try:
        client.db_create(
           db,
           pyorient.DB_TYPE_GRAPH,
           pyorient.STORAGE_TYPE_PLOCAL)
       #logging.info("neomeetup1 Database Created.")
    except pyorient.PyOrientException as err:
       #logging.critical(
       #   "Failed to create neomeetup DB: %" 
       #   % err)
        print(err, "\n err while resetting")
        
def _my_callback(for_every_record):
    print(for_every_record)        


# In[13]:


if client.db_exists(db):
   # Open Database
    print("opening db: {}".format(db))
    try:
        client.db_open(db, my_auth, my_auth)
    except pyorient.PyOrientException as err:
        print(err)
        
else:
    try:
        client.db_create(
           db,
           pyorient.DB_TYPE_GRAPH,
           pyorient.STORAGE_TYPE_PLOCAL)
       #logging.info("neomeetup1 Database Created.")
    except pyorient.PyOrientException as err:
       #logging.critical(
       #   "Failed to create neomeetup DB: %" 
       #   % err)
        print(err)


# In[17]:


df=pd.read_csv("../csv/struttura/member.csv")
df.head()


# In[14]:


go=False
if go:
    start_t=time.time()
    n=10
    debug=True
    n_start=1
    for line in df.itertuples():
        if debug:
            if line.Index > n_start:
                client.command(
           "create VERTEX Member set member_id = {}, member_name = '{}'".format(line.member_id, str(line.member_name).replace("\"", "").replace("'",""))
                )
        else:
            client.command(
           "create VERTEX Member set member_id = {}, member_name = '{}'".format(line.member_id, str(line.member_name).replace("\"", "").replace("'",""))
                )
        if line.Index == n:
            print("reached line {} in {}".format(n, time.time()-start_t))
            break
    result = client.command("select from Member where member_id = 6 ", 100)
    result #lol useless but will find out


# In[20]:


reset_db(client, db)
try:
    client.command( "create class Member extends V" )
except pyorient.PyOrientException as e:
    print(e)


# In[21]:


#stop=True
stop=False

#skip=True
skip=False

#verbose=True
verbose=False

n=20000
n_skip=400000 #just debug purpose
n_stop=100000

start_t=time.time()

batch_query=['begin']
for line in df.itertuples():
    if not skip:
        query="create VERTEX Member set member_id = {}, member_name = '{}'".format(line.member_id, str(line.member_name).replace("\"", "").replace("'",""))
        query.encode("utf-8")
        batch_query.append(query)
    
        if line.Index is not 0:
            if line.Index % n == 0:
                batch_query.append("commit retry 100")
                cmd=';'.join(batch_query)
                if verbose: print("line is ", line.Index)
                print("committing", end= "")
                m_time=time.time()
                client.batch(cmd)
                print("...", end= "")

                if verbose: print("committed in {} s".format((time.time()-m_time)))

                batch_query=['begin']
    else:
        if line.Index >= n_skip:
            query="create VERTEX Member set member_id = {}, member_name = '{}'".format(line.member_id, str(line.member_name).replace("\"", "").replace("'",""))
            query.encode("utf-8")
            batch_query.append(query)

            if line.Index % n == 0:
                batch_query.append("commit retry 100")
                cmd=';'.join(batch_query)
                if verbose: print("line is ", line.Index)
                print("committing", end= "")
                m_time=time.time()
                client.batch(cmd)
                print("...", end= "")
                if verbose: print("committed in {} s".format((time.time()-m_time)))
                
                batch_query=['begin']
    if stop:
        if skip:
            if line.Index == n_stop+n_skip:
                print("reached line {} in {} s".format(line.Index, (time.time()-start_t)*1000))
                print("breaking")
                break
        else:
            if line.Index == n_stop:
                print("reached line {} in {} s".format(line.Index, (time.time()-start_t)*1000))
                print("breaking")
                break
            

if not stop:
    print("reached line {} in {} s".format(len(df), (time.time()-start_t)*1000))

#batch_query.append("commit retry 100")
#cmd=';'.join(batch_query)
#cmd


# In[ ]:


result = client.query_async("select from Member",100, '*:0', _my_callback)


# In[ ]:


len(df)


# In[ ]:


df.head(360165).tail(6)


# In[ ]:




