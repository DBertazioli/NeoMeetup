#!/usr/bin/bash

#directory with csv file
CSV_DIR="/root/NeoMeetup/Csv"
#neo csv import directory 
NEO_IMPORT="/var/lib/neo4j/import"
#path/to/yourscripts
SCRIPT_DIR="/root/NeoMeetup/CypherScripts"

##useful alias 
#alias=false if no alias required
alias=false 
if $alias
then
	if grep "alias cypher" ~/.bashrc
	then echo "cypher ok"
	else 
    		read -p "neo4j pswd: " passwd
    		read -p "reimmit pswd: " passwd1
    
	    	if [ "$passwd0" -a "$passwd1" ]
	    	then 'echo "alias cypher='cypher-shell -u neo4j -p $PSWD --debug --format verbose'">>~/.bashrc'; source ~/.bashrc  
	    	else  echo "password doesn't coincide"; exit 
	    	fi
	fi
fi

#SET_COPY=true per creare symb links dei csv nell'import di default di neo
SET_COPY=true
if $SET_COPY 
then echo "sync dirs"; rsync  ${CSV_DIR}/  ${NEO_IMPORT}/
else echo "dir already sync" 
fi

FAIL=0

echo "importing members"

cat ${SCRIPT_DIR}/create_members_from_csv.cql |nohup bash -ci 'cypher' &

wait `jobs -p` || let "FAIL+=1"

cat ${SCRIPT_DIR}/groups_from_csv.cql |nohup bash -ci 'cypher' & >> out1.out

wait `jobs -p` || let "FAIL+=1"

#remember to add the new .cql (or maybe not? depending on what we actually want with declared topics and stuffs)
: '
echo "importing events"
cat ${SCRIPT_DIR}/events_from_csv.cql |bash -ci 'cypher'
echo "importing venues"
cat ${SCRIPT_DIR}/venues_from_csv.cql |bash -ci 'cypher'
echo "importing topics"
cat ${SCRIPT_DIR}/create_topics_from_csv.cql |bash -ci 'cypher'
echo "importing relations between event and group"
cat ${SCRIPT_DIR}/relation_event_group.cql |bash -ci 'cypher'
echo "importing relations event-venue"
cat ${SCRIPT_DIR}/relation_event_venue.cql |bash -ci 'cypher'
echo "importing relations group-topics"
cat ${SCRIPT_DIR}/relation_group_topics.cql |bash -ci 'cypher'
echo "importing relations member-events"
cat ${SCRIPT_DIR}/relation_member_event.cql |bash -ci 'cypher'
echo "importing relations member-group"
cat ${SCRIPT_DIR}/relation_member_group.cql |bash -ci 'cypher'
echo "importing relations member-group"
cat ${SCRIPT_DIR}/relation_member_topics.cql |bash -ci 'cypher'
'

if [ "$FAIL" == "0" ];
then
echo "YAY!"
else
echo "FAIL! ($FAIL)"
fi


