#!/bin/bash


echo " ~gathering all your information ~"

python virus_getter.py --file 09-16-2019_grapevine.gbc.xml

python country_getter.py --file 09-16-2019_grapevine.gbc.xml



