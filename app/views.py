from flask import Flask, render_template, redirect, url_for, json, request, session, flash, send_file
from flask.ext.mysqldb import MySQL
from app import app

from app.models import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
	
@app.route('/login', methods=['POST'])
def login():
	return render_template('login.html')
	
@app.route('/register')
def register():
	return render_template('register.html')
	
@app.route('/signUp', methods=['POST'])
def signUp():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	if _name and _email and _password:
		return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
		
@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("select 1").all():
		return 'it works.'
	else:
		return 'something is broken.'