# -*- coding: utf-8 -*-
# 02.12.2020, created by Egor Eremenko
import sys
from flask import Flask, request, redirect, url_for, jsonify
import codecs

DEBUG = True
week_config_filename = u'data.json'

def debug_convert_cfg_json(decoded_data):
    '''

    :param decoded_data:
    :return: json с добавкой "data = '[" для чтения конфига через json+js
    '''

    try:
        decoded_data = u"data = '[" + str(decoded_data) + "]';"
    except TypeError as e:
        print('Ошибка при склейке json и строки')
    return decoded_data

def save_to_file(filename, data):
    print(filename, 'file will be saved')
    try:
        f = codecs.open(filename, 'w+', encoding='utf8')
    except OSError as e:
        print(' can''t open file ', filename)
        return False

    if DEBUG:
        print('save_to_file data:', data)
    try:
        data = data.decode('utf-8')
    except UnicodeError:
        print(u'Ошибка unicode при конвертации')
        return False

    try:
        if DEBUG:
            f.write(debug_convert_cfg_json(data))
        else:
            f.write(data)
    except OSError:
        print(u' can''t write to file ', filename)
        return False
    finally:
        f.close()

    return True


app = Flask(__name__)

@app.route('/configsuccess')
def configsuccess():
    return u'Файл урока принят и сохранён.'

@app.route('/configfail')
def configfail():
    return u'Файл урока не был сохранён.'

@app.route('/')
def hello_world():
    return u'Hello World!!'


@app.route('/', methods=['POST'])
def result():
    # print(request.form['foo']) # should display 'bar'
    print(request.json, file=sys.stderr)

    if save_to_file(week_config_filename, request.data):
        return jsonify({"redirect": "configsuccess"})
    else:
        return jsonify({"redirect": "configfail"})



if __name__ == '__main__':
    app.run(debug=True)
