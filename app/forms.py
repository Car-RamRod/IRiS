from flask.ext.wtf import Form
from app import app
from wtforms import StringField, SelectField, TextAreaField, DateTimeField, BooleanField, TextAreaField, PasswordField, IntegerField, validators, SubmitField
from wtforms.validators import DataRequired, Length, IPAddress, MacAddress, Optional

class NewAlertForm(Form):
	resource_type = StringField('Resource Type',validators=[DataRequired()])
	source = StringField('Source',validators=[DataRequired()])
	status = StringField('Status',validators=[Optional()])


class UpdateAlertForm(Form):
        status = SelectField('Status', choices=app.config['ASTATUS_CHOICES'])
        atype = StringField('Type')
        ip = StringField('IP Address',validators=[Optional(),IPAddress("Bad IP Address")])
        mac = StringField('MAC Address',validators=[Optional(), MacAddress("Bad Mac Address")])
        comments = TextAreaField('Comments')

class NewIncidentForm(Form):
	title = StringField('Title',validators=[DataRequired()])
	itype = SelectField('Type', choices=app.config['ITYPE_CHOICES'], validators=[DataRequired()])
	#ip = StringField('IP Address',validators=[Optional(),IPAddress("Bad IP Address")])
	#mac = StringField('MAC Address',validators=[Optional(), MacAddress("Bad Mac Address")])
	comments = TextAreaField('Comments')

class UpdateIncidentForm(Form):
	#status = SelectField('Status', choices=[('',''),('Resolved','Resolved'),('Updated','Updated')])
	status = SelectField('Status', choices=app.config['ISTATUS_CHOICES'])
	itype = SelectField('Type', choices=app.config['ITYPE_CHOICES'])
	#ip = StringField('IP Address',validators=[Optional(),IPAddress("Bad IP Address")])
	#mac = StringField('MAC Address',validators=[Optional(), MacAddress("Bad Mac Address")])
	comments = TextAreaField('Comments')


		
