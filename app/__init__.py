from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "fdcf3m3o(H*DNEDAIODNke*@@#NJEDed3"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@localhost/web_project"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bob291070@gmail.com'
app.config['MAIL_PASSWORD'] = 'Something'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
