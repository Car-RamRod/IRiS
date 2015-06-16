IRiS
---------
Incident Response integration System

What is it?
-----------
IRiS allows users to view and manage incidents consisting of relevant
metadata such as IP address(v4/v6), usernames, MAC addresses,
description, time, etc. IRiS can query various network
technologies(Firewall, IPS, etc.) through a RESTful architecture for
alerts that need to be parsed and associated into incidents. Once these
alerts have been enriched and organized into incidents, they will be
inserted into a MongoDB database to be later queried by the IRT. This
database interaction will allow IRT’s to develop patterns and
relationships between incidents and facilitate the ability for an IRT
to quickly respond to threats.




The Latest Version
------------------
Currently in early Alpha.


Documentation
-------------
Currently run on Ubuntu 14.04
The web application currently allows a user to manually enter alerts
and incidents through a web form and stores the data in a MongoDB.

Installation
------------

Install MongoDb
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

Start MongoDB
sudo service mongod start
mongo


Install Flask and related packages
sudo apt-get install python-pip
sudo pip install Flask
sudo pip install flask-wtf
sudo pip install MongoAlchemy
sudo pip install pymongo==2.8

Download IRiS from github
sudo git clone https://github.com/Car-RamRod/IRiS.git

run web server:
run 'python run.py'

Protocol
--------

Licensing
---------
N/A at this time.

Copyright
---------
N/A at this time.

Contacts
--------
Dave Brosnan davebrosnan@mail.adelphi.edu
Jan Masztal janmasztal@mail.adelphi.edu




