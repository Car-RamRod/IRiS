from flask import render_template, redirect, url_for, request, flash
from datetime import datetime
from app import app
from forms import NewAlertForm, UpdateAlertForm, NewIncidentForm, UpdateIncidentForm, PromoteIncidentForm
from models import Alert, Incident, iris_db, IPSAlert
from werkzeug import secure_filename
import os
import csv
import threading, time

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
				title='Home')


@app.route('/alert', methods=['GET', 'POST'])
def alert():

	alerts = iris_db.query(Alert)

	if request.method == 'POST':
		if request.form['btn'] == 'New':
			return redirect(url_for('new_alert'))
	
		elif request.form['btn'] == 'Update':
			selected = request.form.getlist('selected')
			return redirect(url_for('update_alert', selected=selected))
		
		elif request.form['btn'] == 'View':
			selected = request.form.getlist('selected')
			return redirect(url_for('details_alert', selected=selected))
	
	
		elif request.form['btn'] == 'Promote':
			selected = request.form.getlist('selected')
	                return redirect(url_for('promote_incident', 
			    	selected=selected))


        return render_template('alert/alert.html', 
				title='Alert',
			    	alerts=alerts)

@app.route('/details_alert', methods=['GET', 'POST'])
def details_alert():

	selected = request.args.getlist('selected')[0]
	query = iris_db.query(Alert).filter(Alert.idNum == selected)
	return render_template("alert/details_alert.html",
			                                title='Alert Details',
			                                alert=query[0].represent())




@app.route('/new_alert', methods=['GET', 'POST'])
def new_alert():
	form = NewAlertForm()
        #mongoalchemy
        #alerts = session.query(Alert).filter(Alert.name == 'Second_Alert')       

	if form.validate_on_submit():
                resource_type = form.resource_type.data
                source = form.source.data
                status = form.status.data
                timestamp = datetime.utcnow()
                idNum = str(timestamp)
	        comments = [""]
        
                #mongoalchemy
                iris_db.insert(Alert(resource_type=resource_type,
					source=source,
					status=status,
					timestamp=timestamp,
                                        idNum=idNum,
                                        comments=comments))
                return redirect(url_for('alert'))


        return render_template("alert/new_alert.html",
                                title='New Alert',
				form=form)

@app.route('/update_alert', methods=['GET', 'POST'])
def update_alert():
	alerts = []
	form= UpdateAlertForm()

	selected = request.args.getlist('selected')
	print selected
	for s in selected:
		query = iris_db.query(Alert).filter(Alert.timestamp == s)
		for q in query:
			d = {
				'resource_type':q.resource_type,
				'source':q.source,
				'status':q.status,
				'timestamp':q.timestamp,
				}
		alerts.append(d)

	if request.method == 'POST':
		update = request.form.getlist('update')
	
		if update:
		
			alert = iris_db.query(Alert).filter(Alert.timestamp == update[0])
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
	incidents = iris_db.query(Incident)

	if request.method == 'POST':
		if request.form['btn'] == 'New':
			return redirect(url_for('new_incident'))
		elif request.form['btn'] == 'Update':
			selected = request.form.getlist('selected')
			return redirect(url_for('update_incident', selected=selected))
		elif request.form['btn'] == 'View':
			selected = request.form.getlist('selected')
			return redirect(url_for('details_incident', selected=selected))
	
	return render_template('incident/incident.html', 
				title='Incident',
				incidents=incidents)


		#return redirect(url_for('incident'))
	#return render_template('incident.html',
	#			title='Incident',
	#			incidents=incidents,
	#			form=form)

@app.route('/promote_incident',methods=['GET', 'POST'])
def promote_incident():
    selected = request.args.getlist('selected')
    res = ()
    
    for s in selected:
        query = iris_db.query(Alert).filter(Alert.idNum == s)
        for q in query:
            res += q.promote()


    form = PromoteIncidentForm()
    if form.validate_on_submit():
        title = form.title.data
        itype = form.itype.data
        entered = datetime.utcnow()
        comments = [form.comments.data]
        resources = res
        
        iris_db.insert(Incident(title=title,
                                    status="Promoted",
                                    itype=itype,
                                    comments=comments,
                                    entered=entered,
                                    resources=resources))
        return redirect(url_for('incident'))

    return render_template("incident/new_incident.html",
                                title='New Incident',
				form=form)

       

@app.route('/details_incident', methods=['GET', 'POST'])
def details_incident():

	selected = request.args.getlist('selected')[0]
	query = iris_db.query(Incident).filter(Incident.title == selected)
	
	return render_template("incident/details_incident.html",
			                                title='Incident Details',
			                                incident=query[0])


@app.route('/new_incident', methods=['GET', 'POST'])
def new_incident():

	form = NewIncidentForm()
	if form.validate_on_submit():
                title = form.title.data
                itype = form.itype.data
                entered = datetime.utcnow()
                comments = [form.comments.data]
		resources = []

				
                iris_db.insert(Incident(title=title,
                                        status="Manual",
                                        itype=itype,
                                        comments=comments,
                                        entered=entered,
					resources=resources)
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
			resource_type = r['resource_type']
			source = r['source']
			status =  r['status']	
			timestamp = datetime.utcnow()
			idNum = r['idNum']
			comments = [r['comments']]
	
			iris_db.insert(Alert(resource_type=resource_type,
						source=source,
						status=status,
						timestamp=timestamp,
						idNum=idNum,
						comments=comments))


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():

	if request.method == 'POST':
		file = request.files['file']
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

#new thread to check and parse files in uploads folder
#note example scp to act as if there is a cron or sompthing placing files in the folder
#scp /home/user/Desktop/log.csv /home/user/Desktop/log1.csv /home/user/Desktop/log2.csv ramrod@192.168.1.15:/home/ramrod/IRiS/app/uploads
#note need to call the interupt method with the app closes
time_wait = 60
data_lock = threading.Lock()
parse_thread = threading.Thread()

def interrupt():
	global parse_thread
	parse_thread.cancel()


def check_uploads():
	global parse_thread
	with data_lock:
		files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
		if(files != None):
			for f in files:
				if allowed_file(f):
					parse_upload(app.config['UPLOAD_FOLDER'], f)
					os.remove(os.path.join(app.config['UPLOAD_FOLDER']+'/'+f))
				else:
					os.remove(os.path.join(app.config['UPLOAD_FOLDER']+'/'+f))
		parse_thread = threading.Timer(time_wait, check_uploads, ())
		parse_thread.start()

check_uploads()
