from flask import Flask, render_template, redirect, url_for, json, request, session, flash, send_file
from flask.ext.mysqldb import MySQL
from app import app

from app.models import db, User, Task
from app.forms import SignupForm, SigninForm, AddTaskForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = AddTaskForm()
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('index.html', form=form)
		else:
			_task_user_id = None #form.task_user_id.data
			_task_date = "01/01/70" #form.task_date.data
			_task_address = "768 Vista Drive" #form.task_address.data
			newtask = Task(form.task_title.data, form.task_description.data, _task_date, _task_address)
			db.session.add(newtask)
			db.session.commit()
			
			session['task_title'] = newtask.task_title
			session['task_description'] = newtask.task_description
			
			return redirect(url_for('index'))
			
	elif request.method == 'GET':
		return render_template('index.html', form=form)
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	
	if 'email' in session:
		return redirect(url_for('profile'))
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('register.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			
			session['email'] = newuser.email
			return redirect(url_for('profile'))
			return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
		
	elif request.method == 'GET':
		return render_template('register.html', form=form)

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))
	
	user = User.query.filter_by(email = session['email']).first()
	
	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')
	
@app.route('/signin', methods=['GET', 'POST'])	
def signin():
	form = SigninForm()
	
	if 'email' in session:
		return redirect(url_for('profile'))
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))
			
	elif request.method == 'GET':
		return render_template('login.html', form=form)

@app.route('/signout')
def signout():

	if 'email' not in session:
		return redirect(url_for('signin'))
		
	session.pop('email', None)
	return redirect(url_for('index'))
	
# @app.route('/register')
# def register():
	# return render_template('register.html')
	
# @app.route('/signUp', methods=['POST'])
# def signUp():
	# _name = request.form['inputName']
	# _email = request.form['inputEmail']
	# _password = request.form['inputPassword']
	# if _name and _email and _password:
		# return json.dumps({'html':'<span>All fields good !!</span>'})
	# else:
		# return json.dumps({'html':'<span>Enter the required fields</span>'})
		
