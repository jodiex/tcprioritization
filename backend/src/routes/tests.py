from flask import Blueprint

tests = Blueprint('tests', __name__)

@tests.route('/', methods=['GET'])
def getTests():
    return 'Hello World!'

@tests.route('/<test>', methods=['GET'])
def getTest(test):
    pass

