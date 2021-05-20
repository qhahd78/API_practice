from flask import Flask, request, render_template
from api.py import ApiTest
import requests

# from test import 
app = Flask(__name__)

@app.route('/', methods=["GET"])
def index(): 
    # name = request.form['h']
    return render_template('index.html')

@app.route('/info', methods=["GET"])
def info():
    # form  값 받아옴 
    if request.method == 'GET':
        hour = request.args.get('h')
        dict = ApiTest(hour)

    
    return render_template('info.html', dict = dict)

