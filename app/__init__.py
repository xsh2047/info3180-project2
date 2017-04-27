from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = "fdcf3m3o(H*DNEDAIODNke*@@#NJEDed3"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lab5:password@localhost/lab5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
UPLOAD_FOLDER = './app/static/uploads'

db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
