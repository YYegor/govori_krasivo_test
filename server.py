# -*- coding: utf-8 -*-
# 02.12.2020, created by Egor Eremenko
import sys
from flask import Flask, request, jsonify, render_template, url_for

import datetime as dt
from werkzeug.routing import BaseConverter
from flask import send_from_directory
import os
import logo_stuff as ls
import config as cfg

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
# включить поддержку regex
app.url_map.converters['regex'] = RegexConverter


def audio_full_path_gen(user_uid='', file_ext=u'webm', filename_prefix=u'a'):
    timestamp = dt.datetime.now().strftime("%y%m%d_%H%M%S_%f")
    return cfg.audio_folder + u'\\' + str(filename_prefix) + u'_' + str(user_uid) + u'_' + timestamp + u'.' + str(
        file_ext)


def save_audio_to_file(audio_filename, data):
    print(u'Сохраняем аудио ', audio_filename)
    try:
        f = open(audio_filename, 'wb')
    except OSError as e:
        print(u'Не смог открыть на запись файл ', audio_filename)
        return False

    if cfg.DEBUG:
        print(u'save_audio_to_file данные:', type(data))

    try:
        f.write(bytes(data))
    except OSError:
        print(u'Не смог записать данные аудио в ', audio_filename)
        return False
    finally:
        f.close()

    return True

@app.route('/save_audio', methods=['POST'])
def user_audio_save():
    print(u'mime: ', request.mimetype, file=sys.stderr)
    print(u'get data: ', request.get_data(), file=sys.stderr)
    print(u'get json: ', request.get_json(), file=sys.stderr)
    # print(u'get form: ', type(request.files['audio']), file=sys.stderr)

    # TODO: try catch
    uid = str(request.form['uid'])

    # создать имя файла
    filename = audio_full_path_gen(user_uid=uid)

    try:
        request.files['audio'].save(filename)
    except OSError as e:
        print(u'Ошибка сохранения аудио %s на диск')
        return jsonify({"redirect": "configfail"})

    return jsonify({"redirect": "configsuccess"})



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ключ для пользователя для страницы
@app.route('/<regex("[a-f0-9]{7}"):uid>')
def user_week_config_open(uid):
    # return u'Пользователь %s' % (uid)
    print(u'data_' + str(uid) + '.json')
    return render_template('user_week_template.html', config_path=u'data_' + str(uid) + '.json', uid=uid)


@app.route('/')
def user_hello_server():
    return u'Сервер готов'


# подключение модуля логопеда
app.register_blueprint(ls.logo_cabinet_bp)
app.register_blueprint(ls.logo_text_bp)
app.register_blueprint(ls.logo_save_week_bp)
app.register_blueprint(ls.logo_save_success_bp)
app.register_blueprint(ls.logo_save_fail_bp)



if __name__ == '__main__':
    app.run(debug=True)
