#!/usr/bin/env python
# coding: utf-8


from flask import Flask
from flask import request
from flask import *

app = Flask(__name__)


@app.route('/')
def student():
    return render_template("flask_search_partial.html")


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        return render_template("result_flask_search_partial.html",result = result)



app.run()
