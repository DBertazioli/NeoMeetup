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
debug_cont=1
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
        count=0
        #count=None
        excp_count=0
        print "requesting at http://api.meetup.com/2/members"        

        #for line in member_df.itertuples():           #basic iter
        #for x, y in pairwise(member_df.itertuples()): #pairs iter
            
        #request parameters	
        per_page = 1
        #results_we_got = per_page #more pages output
        offset = 0 
        for i in range (295,305):
            id_0=member_ids[i]
            print "#####\n "+ str(i)+"-th request of id: "+ str(id_0) + "\n######"
            response0=get_results({"member_id":id_0, "key":max_key, "page":per_page, "offset":offset})
            print response0        
            data0=response0['results']
            #print data0
            for elem in data0:
                #print elem
                if elem['topics']:
                    #print elem['topics']
                    topic_list=[]
                    for e in elem['topics']:
                        a=json.dumps(e)
                        b=json.loads(a) #unicode prob
                        #print b['urlkey']
                        topic_list.append(str(b['urlkey']).encode('utf-8'))

def get_results(params):

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
        pass
     
    return data


if __name__=="__main__":
        main()

