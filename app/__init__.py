from flask import Flask

app = Flask(__name__)
app.secret_key = 'ayylmao'
from app import views

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://velvokay:alpine64@mysql.server/velvokay$default'
 
from app.models import db
db.init_app(app)