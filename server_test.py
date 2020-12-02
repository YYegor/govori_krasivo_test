# -*- coding: utf-8 -*-
# 02.12.2020, created by Egor Eremenko
import sys
from flask import Flask, request


def save_to_file(filename, data):
    print("file will be saved")
    return


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/', methods=['POST'])
def result():
    #print(request.form['foo']) # should display 'bar'
    print(request.data, file=sys.stderr)
    save_to_file('config_test.txt', request.data)
    return 'Received !' # response to your request.

if __name__ == '__main__':
    app.run(debug=True)