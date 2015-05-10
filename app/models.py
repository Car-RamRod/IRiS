from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
from datetime import  datetime

class Alert(Document):
	config_collection_name = 'alert'

	resource_type = StringField()
	source = StringField()
	status = StringField()
	timestamp = DateTimeField()
	comments = ListField(AnythingField())	

	def promote(self):
		source = Source(self, self.source)
		return source

class IPSAlert(Alert):
	ip_src = StringField()
	ip_dst = StringField()
	port_src = StringField()
	port_dst = StringField()
	
	def promote(self):	
		socket = Socket(self, self.ip_src, self.port_src)
		return socket


class Resource(Field):
        creation_datetime = None
        creator = None




class Source(Resource):
        alert_id = None
        source = None

        def __init__(self,parent,source):
                self.alert_id = parent.mongo_id
		self.source = source

class Socket(Resource):
	alert_id = None
	ip = None
	port = None

	def __init__(self, parent,  ip, port):
		self.alert_id = parent.mongo_id
		self.ip = ip
		self.port = port
	
	
class Incident(Document):
	config_collection_name = 'incident'
	resource = ListField(AnythingField())


iris_db = Session.connect('iris_db')

#will clear collection when python  run.py
iris_db.clear_collection(Alert)
iris_db.clear_collection(Incident)

