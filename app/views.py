from flask import Flask, render_template, redirect, url_for, json, request, session, flash, send_file
from flask.ext.mysqldb import MySQL
from app import app

from app.models import db, User
from app.forms import SignupForm, SigninForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
	
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

@app.route('/addTask',methods=['POST'])
def addTask():
	try:
        if session.get('email'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('email')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addTask',(_title,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return redirect('/index')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

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
		
