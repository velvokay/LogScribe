from flask import Flask, render_template, redirect, url_for, json, request, session, flash, send_file
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
	