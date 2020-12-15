# -*- coding: utf-8 -*-
# 02.12.2020, created by Egor Eremenko
import sys
from flask import Flask, request, redirect, url_for, jsonify
import codecs

DEBUG = True
week_config_filename = u'data.json'
audio_filename = u'audio.webm'

def debug_convert_cfg_json(decoded_data):
    '''

    :param decoded_data:
    :return: json с добавкой "data = '[" для чтения конфига через json+js
    '''

    try:
        decoded_data = u"data = '[" + str(decoded_data) + "]';"
    except TypeError as e:
        print(u'Ошибка при склейке json и строки конфига недели')
    return decoded_data


def save_audio_to_file(audio_filename, data):
    print(u'Сохраняем аудио ', audio_filename)
    try:
        f = open(audio_filename, 'wb')
    except OSError as e:
        print(u'Не смог открыть на запись файл ', audio_filename)
        return False

    if DEBUG:
        print(u'save_audio_to_file данные:', type(data), data)

    try:
        f.write(data)
    except OSError:
        print(u'Не смог записать данные аудио в ', audio_filename)
        return False
    finally:
        f.close()

    return True


def save_week_conf_to_file(filename, data):
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
        f.close()
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
    return u'Файл урока не был сохранён из-за ошибки.'

@app.route('/')
def hello_server():
    return u'Сервер готов'


@app.route('/save_audio', methods=['POST'])
def result_audio():
    print('mime: ', request.mimetype, len(request.mimetype),  file=sys.stderr)
    print('data: ', request.get_data(), file=sys.stderr)

    if save_audio_to_file(audio_filename, request.get_data()):
        return jsonify({"redirect": "configsuccess"})
    else:
        return jsonify({"redirect": "configfail"})

@app.route('/', methods=['POST'])
def result():
    if save_week_conf_to_file(week_config_filename, request.data):
        return jsonify({"redirect": "configsuccess"})
    else:
        return jsonify({"redirect": "configfail"})



if __name__ == '__main__':
    app.run(debug=True)
