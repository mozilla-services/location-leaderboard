#!/bin/bash
apt-get --assume-yes install unzip 

# Source http://thematicmapping.org/downloads/
# License http://creativecommons.org/licenses/by-sa/3.0/
wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
unzip TM_WORLD_BORDERS-0.3.zip

./manage.py load_countries ./TM_WORLD_BORDERS-0.3.shp
