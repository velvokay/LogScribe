from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
	
class Task(db.Model):
	__tablename__ = 'tbl_task'
	task_id = db.Column(db.Integer, primary_key = True)
	task_title = db.Column(db.String(45))
	task_description = db.Column(db.String(5000))
	task_user_id = db.Column(db.Integer)
	task_date = db.Column(db.DateTime)
	task_address = db.Column(db.String(80))
	
	def __init__(self, task_title, task_description, task_date, task_address):
		self.task_title = task_title.title()
		self.task_description = task_description.title()
		self.task_date = task_date.lower()
		self.task_address = task_address.lower();