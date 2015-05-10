from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *


class Field:
    def __init__(self, name, elements):
        self.name = name
        if not isinstance(elements,list):
            self.elements = [elements]
        else:
            self.elements = elements



class Alert(Document):
	config_collection_name = 'alert'

	title = StringField()
	status = StringField()
	atype = ListField(AnythingField())
#	alert_generated = DateTimeField()
	entered = DateTimeField()
	ip = ListField(AnythingField())
        mac = ListField(AnythingField())
	comments = ListField(AnythingField())

	def __str__(self):
		return '%s %s %s' % (self.title, self.status,self.ip)

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

class Incident(Document):
	config_collection_name = 'incident'
	
	#incident_title = StringField()
	title = StringField()
	status = StringField()
	##idNum = StringField()
	itype = StringField()
	#itype = ListField(AnythingField())
	#incident_generated = DateTimeField()
	entered = DateTimeField()
	#incident_ip = ListField(AnythingField())
	#incident_mac = ListField(AnythingField())
	
	comments = ListField(AnythingField())
	
	#alerts = ListField(RefField(type=DocumentField(Alert)))
	resources = ListField(AnythingField())



iris_db = Session.connect('iris_db')

#will clear collection when python  run.py
#iris_db.clear_collection(Alert)
#iris_db.clear_collection(Incident)

