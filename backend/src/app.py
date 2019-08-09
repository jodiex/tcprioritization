from flask import Flask
from routes.tests import tests

app = Flask("QABackend")
app.register_blueprint(tests, url_prefix='/tests')

@app.route('/')
def HelloWordl():
    return "Hello World!"



print(__name__)
    #app.run()
