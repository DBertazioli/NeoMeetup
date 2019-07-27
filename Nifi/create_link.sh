#!/bin/bash
echo "creating link dir"
#mkdir /tmp/rsvp-data-april_link0
mkdir /tmp/rsvp-data-april_link1
mkdir /tmp/rsvp-data-april_link2
mkdir /tmp/rsvp-data-april_link3

echo "giving permission to data (for nifi)"
#chmod -R 777 /tmp/rsvp-data-april
#chmod -R 777 /root/rsvp-data-april

echo "creating symbolic links"
cp -rs /root/rsvp-data-april/ /tmp/rsvp-data-april_link0/

echo "moving to /tmp/rsvp-data-april_link0"
cd /tmp/rsvp-data-april_link0

echo "splitting the main folder"
ls -1 | sort -n | head -500000 | xargs -i mv "{}" /tmp/rsvp-data-april_link1
ls -1 | sort -n | head -500000 | xargs -i mv "{}" /tmp/rsvp-data-april_link2
ls -1 | sort -n | head -500000 | xargs -i mv "{}" /tmp/rsvp-data-april_link3

echo "giving permission to data (for nifi)"
chmod -R 777 /tmp/rsvp-data-april_link0
chmod -R 777 /tmp/rsvp-data-april_link1
chmod -R 777 /tmp/rsvp-data-april_link2
chmod -R 777 /tmp/rsvp-data-april_link3


