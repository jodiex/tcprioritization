from flask import Flask
from routes.tests import tests
from flask_cors import CORS

app = Flask("QABackend")
CORS(app)

app.register_blueprint(tests, url_prefix='/tests')

@app.route('/')
def HelloWordl():
    return "Hello World!"
