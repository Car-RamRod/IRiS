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
	idNum = StringField()
        comments = ListField(AnythingField())	

	def represent(self):
		items = []

                items.append(Field("Resource Type", self.resource_type))
                items.append(Field("Status", self.status))
                items.append(Field("Source", self.source))
                items.append(Field("Date Entered", self.timestamp))
                #items.append(Field("IP Address", self.ip))
                #items.append(Field("MAC Address", self.mac))
                items.append(Field("Comments", self.comments))
	
                return items
            

	def promote(self):
            timeRes = Timestamp(self, self.timestamp)
            sourceRes = SourceDev(self, self.source)
            return (timeRes, sourceRes)


class IPSAlert(Alert):
	ip_src = StringField()
	ip_dst = StringField()
	port_src = StringField()
	port_dst = StringField()
	
	def promote(self):	
                parTup = Alert.promote()
		socket = Socket(self, self.ip_src, self.port_src)
		return parTup + socket


class Resource(Document):
    parent = ''

        
class Timestamp(Resource):
    stamp = ''

    def __init__(self, parent, stamp):
        self.stamp = stamp
        self.parent = Resource.mongo_id

class SourceDev(Resource):
    sourceDev = ''

    def __init__(self, parent, sourceDev):
        self.sourceDev = sourceDev
        self.parent = Resource.mongo_id

class Socket(Resource):
	alert_id = None
	ip = None
	port = None

	def __init__(self, parent,  ip, port):
		self.alert_id = Resource.mongo_id
		self.ip = ip
		self.port = port
	

class Incident(Document):
	config_collection_name = 'incident'
        title = StringField()
        status = StringField()
        itype = StringField()
        entered = DateTimeField()
	resources = ListField(DocumentField(Resource))
        comments = ListField(AnythingField())

iris_db = Session.connect('iris_db')

#will clear collection when python  run.py
#iris_db.clear_collection(Alert)
#iris_db.clear_collection(Incident)

