#!/usr/bin/env python
# coding: utf-8

# In[139]:


#!/usr/bin/env python


# coding: utf-8
from __future__ import unicode_literals
import sys
try:
    import requests
except ImportError:
    get_ipython().system('python2 -m pip install requests')
    import requests
    
import json
import time
import codecs
import sys
try:
    import pandas as pd 
except ImportError:
    get_ipython().system('python2 -m pip install pandas')
    import pandas as pd
try:
    import numpy as np
except ImportError:
    get_ipython().system('python2 -m pip install numpy')
    import numpy as np

from itertools import izip #iter pairwise
from itertools import izip_longest #iter over tuples


# In[140]:


#import yaml #alternative solution for json probs
#UTF8Writer = codecs.getwriter('utf8') #toUtf8 stuffs, nevermind
#sys.stdout = UTF8Writer(sys.stdout)


# In[141]:


#debug=1
debug=0
debug_count=1
#count_stopper=100


# In[142]:


member_df=pd.read_csv("../csv/struttura/member.csv")
print member_df.head(2)


# In[143]:


member_ids=member_df['member_id']
member_df['topics']="err"
member_df['lat']=0.
member_df['long']=0.
print member_df.head()


# In[144]:


#remember to hide it after 
fabri_key="2e12625a12642d6ac743d19566c393e"
max_key="445811b5a6b424f7e79342826176d"
my_api_key= "546938372953301546964e404246e"


# In[145]:


#not really working but who cares 
block_alert={u'problem': u'Client throttled', u'code': u'throttled', u'details': u'Credentials have been throttled'}


# In[146]:


#iterating tuples at once
#old pairs version (to keep in case)
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)


# In[147]:


#more complete groupin version
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


# In[148]:


def main():
        count=0
        tot_count=0
        print "requesting at http://api.meetup.com/2/members"        

        #for line in member_df.itertuples():           #basic iter
        #for x, y in pairwise(member_df.itertuples()): #pairs iter
        for z in grouper(member_df.itertuples(),3): #groups
            
            #request parameters	
            per_page = 1
            #results_we_got = per_page #more pages output
            offset = 0            
       
            #get id (one should really vectorize it)
            id_0=member_df.iloc[z[0].Index]['member_id']
            id_1=member_df.iloc[z[1].Index]['member_id']
            id_2=member_df.iloc[z[2].Index]['member_id']

            # Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/
            try:    
                response0=get_results({"member_id":id_0, "key":max_key, "page":per_page, "offset":offset}, tot_count,1)
                time.sleep(0.05) #PLS U NO BAN me
            
                response1=get_results({"member_id":id_1, "key":my_api_key, "page":per_page, "offset":offset}, tot_count,2)
                time.sleep(0.05) #PLS U NO BAN me
            
                response2=get_results({"member_id":id_2, "key":fabri_key, "page":per_page, "offset":offset}, tot_count,3)
            except Exception as e:
                print "exception encountered at requesting: "
                print e
            time.sleep(0.15) #PLS U NO BAN me
            offset += 1
            #results_we_got = response['meta']['count']              
            #time.sleep(1)
            count+=1
            tot_count+=1
            if debug:
                print "resp 0"
                print response0
                print "resp 1"
                print response1
                print "resp 2"
                print response2
            
            #one should really loop over those
            try:
                data0=response0['results']

                for elem in data0:
                    if elem['topics']:
                        #print elem['topics']
                        topic_list=[]
                        for e in elem['topics']:
                            a=json.dumps(e)
                            b=json.loads(a) #unicode prob
                            #print b['urlkey']
                            topic_list.append(str(b['urlkey']).encode('utf-8'))
                            #print topic_list

                            #c= yaml.safe_load(a) #alternative in case of utf8 representation, keep it just as a reminder
                            #print c['urlkey']

                        #member_df['topics'].at[z[0].Index]=elem['topics'] #get the whole list of dicts 
                        member_df['topics'].at[z[0].Index]=topic_list #get only the topic urlkey list
                    else:
                        member_df['topics'].at[z[0].Index]="NaN"
                    try:
                        if elem['lon']:
                                if elem['lat']:
                                    member_df['long'].at[z[0].Index]=elem['lon']
                                    member_df['lat'].at[z[0].Index]=elem['lat']
                        else:
                            member_df['long'].at[z[0].Index]="NaN"
                            member_df['lat'].at[z[0].Index]="NaN"
                    except: 
                        pass #for the moment lets try this way
                        
            except Exception as e:
                print "exception in response0: "
                print e
                print "is the "+str(count)+"-th iteration"
                try: 
                    print "response is: "
                    print response0
                except:
                    pass
                                                    
            try:
                data1=response1['results']

                for elem in data1:
                    if elem['topics']:
                        #print elem['topics']
                        topic_list=[]
                        for e in elem['topics']:
                            a=json.dumps(e)
                            b=json.loads(a) #unicode prob
                            #print b['urlkey']
                            topic_list.append(str(b['urlkey']).encode('utf-8'))
                            #print topic_list

                            #c= yaml.safe_load(a) #alternative in case of utf8 representation, keep it just as a reminder
                            #print c['urlkey']

                        #member_df['topics'].at[z[0].Index]=elem['topics']
                        member_df['topics'].at[z[1].Index]=topic_list
                    else:
                        member_df['topics'].at[z[1].Index]="NaN"
                    try:
                        if elem['lon']:
                                if elem['lat']:
                                    member_df['long'].at[z[1].Index]=elem['lon']
                                    member_df['lat'].at[z[1].Index]=elem['lat']
                        else:
                            member_df['long'].at[z[1].Index]="NaN"
                            member_df['lat'].at[z[1].Index]="NaN"
                    except: 
                        pass #for the moment lets try this way

            except Exception as e:
                print "exception in response1: "
                print e
                print "is the "+str(count)+"-th iteration"
            try:                                        
                data2=response2['results']

                for elem in data2:
                    if elem['topics']:
                        #print elem['topics']
                        topic_list=[]
                        for e in elem['topics']:
                            a=json.dumps(e)
                            b=json.loads(a) #unicode prob
                            #print b['urlkey']
                            topic_list.append(str(b['urlkey']).encode('utf-8'))
                            #print topic_list

                            #c= yaml.safe_load(a) #alternative in case of utf8 representation, keep it just as a reminder
                            #print c['urlkey']

                        #member_df['topics'].at[z[0].Index]=elem['topics']
                        member_df['topics'].at[z[2].Index]=topic_list
                    else:
                        member_df['topics'].at[z[2].Index]="NaN"
                    try:
                        if elem['lon']:
                                if elem['lat']:
                                    member_df['long'].at[z[2].Index]=elem['lon']
                                    member_df['lat'].at[z[2].Index]=elem['lat']
                        else:
                            member_df['long'].at[z[2].Index]="NaN"
                            member_df['lat'].at[z[2].Index]="NaN"
                    except: 
                        pass #for the moment lets try this way

            except Exception as e:
                print "exception in response2: "
                print e
                print "is the "+str(count)+"-th iteration"
            
            if response0 is block_alert:
                print "throttle alert on response 0 (max key)"
                break
            if response1 is block_alert:
                print "throttle alert on response 1 (my key)"
                break
            if response2 is block_alert:
                print "throttle alert on response 2 (fabri key)"
                break
            if debug_count:
                #if tot_count is count_stopper:
                #    print "breaking"
                #    break
                if count is 50000:
                    print "partial count is"+ str(count)
                    print "csv printed at iteration" + str(tot_count)+" (to be multiplied *3 btw)"
                    member_df.to_csv("../csv/struttura/member_enriched_easter.csv")
                    count=0
            
        print member_df.head()
        print member_df.tail()
        print "exporting to csv"
        member_df.to_csv("../csv/struttura/member_enriched_final.csv") #prolly never reach here sadly but we always hope that member_enriched_final.csv will be identical to member_enriched.csv, that would be mad&amazing


# In[149]:


def get_results(params, tot_count, n):

    request = requests.get("http://api.meetup.com/2/members",params=params)
    try:
        data = request.json()
        #iter_data=json.load(data)
        #a=data['results']
        #for elem in a:
            #print(elem['topics'])
        #print(request)
    except Exception as e:
        print "trying again:"
        time.sleep(0.05)
        try:
            request = requests.get("http://api.meetup.com/2/members",params=params)
            data = request.json()
            print "noice"
        except Exception as e:
            print "failed anyway"
            print "internal exception in loading request.json() at the "+ str(tot_count*3+n) + "iteration"
            print e
            print request
            print request.content
            pass
        pass
        
        
     
    return data


# In[123]:


# In[150]:


if __name__=="__main__":
        main()


# In[ ]:




