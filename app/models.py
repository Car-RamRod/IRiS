from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
from datetime import  datetime

class Field:
    def __init__(self, name, elements):
        self.name = name
        if not isinstance(elements,list):
            self.elements = [elements]
        else:
            self.elements = elements



class Alert(Document):
	config_collection_name = 'alert'

	resource_type = StringField()
	source = StringField()
	status = StringField()
	timestamp = DateTimeField()
	comments = ListField(AnythingField())	

	def represent(self):
		items = []


                items.append(Field("Title", self.title))
                items.append(Field("Status", self.status))
                items.append(Field("Type", self.atype))
                items.append(Field("Date Entered", self.entered))
                items.append(Field("IP Address", self.ip))
                items.append(Field("MAC Address", self.mac))
                items.append(Field("Comments", self.comments))
	
                return items
            

	def __repr__(self):
		'''

		msg = "Title: %s;" % (self.title)
		msg += "Status: %s;" % (self.status)
		msg += "Type: "
		
		for t in atype:
			msg += "%s" % (t)


		return "Title: %s
			Status: %s
			Type: %s
			Date Entered: %s
			IP Address: %s
			MAC Address: %s
			Comments: %s" % (
			self.title, self.status, self.atype,
			self.entered, self.ip, self.mac, self.comments
		'''
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

