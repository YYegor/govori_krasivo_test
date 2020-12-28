# -*- coding: utf-8 -*-
# 02.12.2020, created by Egor Eremenko
import sys
from flask import Flask, request, jsonify, render_template
import codecs

from werkzeug.routing import BaseConverter
from werkzeug import secure_filename

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


DEBUG = True
week_config_filename = u'data.json'
audio_filename = u'user_content_audio/audio.webm'

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
        print(u'save_audio_to_file данные:', type(data))

    try:
        f.write(bytes(data))
    except OSError:
        print(u'Не смог записать данные аудио в ', audio_filename)
        return False
    finally:
        f.close()

    return True


def save_week_conf_to_file(filename, data):
    if DEBUG:
        print(filename, 'file will be saved')
    try:
        f = codecs.open(filename, 'w+', encoding='utf8')
    except OSError as e:
        print(' can''t open file ', filename)
        return False

    if DEBUG:
        print('save_week_conf_to_file data:', data)
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
#включить поддержку regex
app.url_map.converters['regex'] = RegexConverter

@app.route('/configsuccess')
def logo_config_success():
    return u'Файл урока принят и сохранён.'

@app.route('/configfail')
def logo_config_fail():
    return u'Файл урока не был сохранён из-за ошибки.'


#ключ для пользователя для страницы
@app.route('/<regex("[a-f0-9]{7}"):uid>')
def user_week_config_open(uid):
    #return u'Пользователь %s' % (uid)
    print (u'data_' + str(uid) + '.json')
    return render_template('user_week_template.html', config_path=u'data_' + str(uid) + '.json', uid=uid)


@app.route('/')
def user_hello_server():
    return u'Сервер готов'


@app.route('/logo_cabinet')
def logo_cabinet():
    return render_template('logo_cabinet.html')

# @app.route('/mic_audio_index')
# def user_mic_test():
#     return render_template('mic_audio_index.html')


@app.route('/save_audio', methods=['POST'])
def user_audio_save():
    print('mime: ', request.mimetype,  file=sys.stderr)
    print('get data: ', request.get_data(), file=sys.stderr)
    print('get json: ', request.get_json(), file=sys.stderr)
    print('get form: ', type(request.files['audio']), file=sys.stderr)
    request.files['audio'].save(audio_filename)

    #if save_audio_to_file(audio_filename, request.files['audio']):
    return jsonify({"redirect": "configsuccess"})
    #else:
    #    return jsonify({"redirect": "configfail"})

@app.route('/', methods=['POST'])
def logo_config_save():
    if save_week_conf_to_file(week_config_filename, request.data):
        return jsonify({"redirect": "configsuccess"})
    else:
        return jsonify({"redirect": "configfail"})



if __name__ == '__main__':
    app.run(debug=True)
