#!/usr/bin/env python


# coding: utf-8
from __future__ import unicode_literals
import sys
import requests
import json
import time
import codecs
import sys

import pandas as pd
import numpy as np

from itertools import izip #iter pairwise
from itertools import izip_longest #iter over tuples

#import yaml #alternative solution for json probs
#UTF8Writer = codecs.getwriter('utf8') #toUtf8 stuffs, nevermind
#sys.stdout = UTF8Writer(sys.stdout)

debug=0
debug_count=0
member_df=pd.read_csv("../Csv/Struttura/member.csv")
print member_df.head(2)

member_ids=member_df['member_id']
member_df['topics']="nan"
#print member_df.head()

#remember to hide it after 
fabri_key="2e12625a12642d6ac743d19566c393e"
max_key="445811b5a6b424f7e79342826176d"
my_api_key= "546938372953301546964e404246e"

#not really working but who cares 
block_alert={u'problem': u'Client throttled', u'code': u'throttled', u'details': u'Credentials have been throttled'}

#iterating tuples at once
#old pairs version (to keep in case)
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

#more complete groupin version
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def main():
        # Get your key here https://secure.meetup.com/meetup_api/key/
        excp_count=0
        count=0
        #count=None
        
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
                response0=get_results({"member_id":id_0, "key":max_key, "page":per_page, "offset":offset}, count, excp_count)
                response1=get_results({"member_id":id_1, "key":my_api_key, "page":per_page, "offset":offset}, count, excp_count)
                response2=get_results({"member_id":id_2, "key":fabri_key, "page":per_page, "offset":offset}, count, excp_count)
            except Exception as e:
                print "exception encountered at requesting: "
                print e
            time.sleep(0.17) #PLS U NO BAN me
            offset += 1
            #results_we_got = response['meta']['count']              
            #time.sleep(1)
            count+=1
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
                        member_df['topics'].at[z[0].Index]=topic_list
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
                        member_df['topics'].at[z[0].Index]=topic_list
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
                print "count is"+ str(count)
                if count is 100:
                    break
            
        print member_df.head()
        print "exporting to csv"
        member_df.to_csv("../Csv/member_enriched.csv")


def get_results(params, count, excp_count):

    request = requests.get("http://api.meetup.com/2/members",params=params)
    try:
        data = request.json()
        #iter_data=json.load(data)
        #a=data['results']
        #for elem in a:
            #print(elem['topics'])
        #print(request)
    except Exception as e:
        print "exception in loading request.json()"
        print e
        print request
        print request.content
        excp_count+=1
        print "is the "+str(excp_count)+"-th exception at the "+ str(count) + "iteration"
        pass
     
    return data


# In[123]:


if __name__=="__main__":
        main()

