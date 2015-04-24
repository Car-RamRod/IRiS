from flask import render_template, redirect, url_for, request, flash
from datetime import datetime
from app import app
from forms import NewAlertForm, UpdateAlertForm, NewIncidentForm, UpdateIncidentForm
from models import Alert, Incident, iris_db
from werkzeug import secure_filename
import os
import csv

header = ['title','status','atype','entered','ip','mac','comments']

@app.route('/')
@app.route('/index')
def index():
	if request.method == 'POST':
                if request.form['btn'] == 'Upload':
                        file = request.files['file']
                        upload_file(file)

	return render_template("index.html",
				title='Home')


@app.route('/alert', methods=['GET', 'POST'])
def alert():

	alerts = iris_db.query(Alert)
	#alerts = []

	if request.method == 'POST':
                if request.form['btn'] == 'Upload':
                        file = request.files['file']
                        upload_file(file)

	if request.method == 'POST':
		if request.form['btn'] == 'New':
			return redirect(url_for('new_alert'))
		elif request.form['btn'] == 'Update':
			selected = request.form.getlist('selected')
			return redirect(url_for('update_alert', selected=selected))
		elif request.form['btn'] == 'Promote':
			selected = request.form.getlist('selected')
			for s in selected:
				query = iris_db.query(Alert).filter(Alert.title == s)
				for q in query:
					alerts.append(q.to_ref())				
					#iris_db.remove(q)

			
			iris_db.insert(Incident(
				title=q.title,
				entered=q.entered,
				comments=q.comments,
				status="Promoted",
				itype=q.itype,
				alerts=alerts
				))
	
	return render_template('alert/alert.html', 
				title='Alert',
				alerts=alerts)


@app.route('/new_alert', methods=['GET', 'POST'])
def new_alert():
	form = NewAlertForm()
	if request.method == 'POST':
                if request.form['btn'] == 'Upload':
                        file = request.files['file']
                        upload_file(file)

        #mongoalchemy
        #alerts = session.query(Alert).filter(Alert.name == 'Second_Alert')       
	new = 'New'
	if form.validate_on_submit():
                title = form.title.data
                ip = [form.ip.data]
                mac = [form.mac.data]
                atype = [form.atype.data]
                entered = datetime.utcnow()
                comments = [form.comments.data]
		
		print title
                #mongoalchemy
                iris_db.insert(Alert(title=title,
                                        ip=ip,
                                        mac=mac,
                                        status=new,
                                        atype=atype,
                                        comments=comments,
                                        entered=entered))
                return redirect(url_for('alert'))


        return render_template("alert/new_alert.html",
                                title='New Alert',
				form=form)

@app.route('/update_alert', methods=['GET', 'POST'])
def update_alert():
	alerts = []
	form= UpdateAlertForm()
	if request.method == 'POST':
                if request.form['btn'] == 'Upload':
                        file = request.files['file']
                        upload_file(file)

	selected = request.args.getlist('selected')
	print selected
	for s in selected:
		query = iris_db.query(Alert).filter(Alert.title == s)
		for q in query:
			d = {
				'title':q.title,
				'status':q.status,
				'atype':q.atype,
				'ip':q.ip,
				'mac':q.mac,
				'entered':q.entered,
				'comments':q.comments,
				}
		alerts.append(d)

	if request.method == 'POST':
		update = request.form.getlist('update')
	
		if update:
		
			alert = iris_db.query(Alert).filter(Alert.title == update[0])
			if form.validate_on_submit():
	    	        	ip = form.ip.data
        		        mac = form.mac.data
				atype = form.atype.data
		                comments = form.comments.data
				status = form.status.data
			
				if status != '':
                                        alert.set(Alert.status,status).execute()

				if atype != '':
                                        alert.extend(Alert.atype,atype).execute()

				if ip != '':
					alert.extend(Alert.ip,ip).execute()
				
				if mac != '':
                                        alert.extend(Alert.mac,mac).execute()

				if comments != '':
                                        alert.extend(Alert.comments,comments).execute()
		
				alerts = iris_db.query(Alert)	
				#note: fix boxes not clearing
				return render_template("alert/update_alert.html",
			                                title='Update Alert',
                        			        form=form,
			                                alerts=alerts)
	return render_template("alert/update_alert.html",
                                title='Update Alert',
				form=form,
				alerts=alerts)

@app.route('/incident', methods=['GET', 'POST'])
def incident():

	if request.method == 'POST':
                if request.form['btn'] == 'Upload':
                        file = request.files['file']
                        upload_file(file)
	
	incidents = iris_db.query(Incident)

	if request.method == 'POST':
		if request.form['btn'] == 'New':
			return redirect(url_for('new_incident'))
		elif request.form['btn'] == 'Update':
			selected = request.form.getlist('selected')
			return redirect(url_for('update_incident', selected=selected))
	
	return render_template('incident/incident.html', 
				title='Incident',
				incidents=incidents)


		#return redirect(url_for('incident'))
	#return render_template('incident.html',
	#			title='Incident',
	#			incidents=incidents,
	#			form=form)

@app.route('/new_incident', methods=['GET', 'POST'])
def new_incident():

	if request.method == 'POST':
                if request.form['btn'] == 'Upload':
                        file = request.files['file']
                        upload_file(file)

	form = NewIncidentForm()
	if form.validate_on_submit():
                title = form.title.data
                itype = form.itype.data
                entered = datetime.utcnow()
                comments = [form.comments.data]
		alerts = []

				
                iris_db.insert(Incident(title=title,
                                        status="Manual",
                                        itype=itype,
                                        comments=comments,
                                        entered=entered,
					alerts=alerts)
					)
                return redirect(url_for('incident'))


        return render_template("incident/new_incident.html",
                                title='New Incident',
				form=form)

@app.route('/update_incident', methods=['GET', 'POST'])
def update_incident():
	incidents = []
	form= UpdateIncidentForm()

	selected = request.args.getlist('selected')
	print selected
	for s in selected:
		query = iris_db.query(Incident).filter(Incident.title == s)
		for q in query:
			d = {
				'title':q.title,
				'status':q.status,
				'itype':q.itype,
				'entered':q.entered,
				'comments':q.comments,
				}
		incidents.append(d)

	if request.method == 'POST':
		if request.form['btn'] == 'Upload':
			file = request.files['file']
			upload_file(file)

		update = request.form.getlist('update')
	
		if update:
		
			incident = iris_db.query(Incident).filter(Incident.title == update[0])
			if form.validate_on_submit():
				itype = form.itype.data
		                comments = form.comments.data
				status = form.status.data
			
				if status != '':
                                        incident.set(Incident.status,status).execute()

				if itype != '':
                                        incident.extend(Incident.itype,itype).execute()

				if comments != '':
                                        incident.extend(Incident.comments,comments).execute()
		
				incidents = iris_db.query(Incident)	
				#note: fix boxes not clearing
				return render_template("incident/update_incident.html",
			                                title='Update Incident',
                        			        form=form,
			                                incidents=incidents)
	return render_template("incident/update_incident.html",
                                title='Update Incident',
				form=form,
				incidents=incidents)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def parse_upload(directory, filename):
	#note: not taking into account that ip,mac,... can be a list or our we forcing one value one column for this
	#note : make a config for the column names and then for loop to add each filed
	with open(directory+'/'+filename) as f:
		records = csv.DictReader(f)
		for r in records:
			title = r['title']
			status = r['status']
			ip =  [r['ip']]	
			mac = [r['mac']]
			atype = [r['atype']]
			entered = datetime.utcnow()
			comments = [r['comments']]

			iris_db.insert(Alert(title=title,
						ip=ip,
						mac=mac,
						status=status,
						atype=atype,
						comments=comments,
						entered=entered))



def upload_file(file):
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('Upload Complete')
		parse_upload(app.config['UPLOAD_FOLDER'], filename)
		return redirect(url_for('upload_file'))
	else:
		flash('Upload Error: Check File Type')
	return render_template('upload_file.html',
				title='Upload File')


