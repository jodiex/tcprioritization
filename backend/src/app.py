from flask import Flask
from routes.tests import tests
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from db.config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
CORS(app)

db = SQLAlchemy(app)

app.register_blueprint(tests, url_prefix='/tests')

@app.route('/')
def HelloWordl():
    return "Hello World!"
