# -*- coding: utf-8 -*-
# 02.12.2020, created by Egor Eremenko
import sys
from flask import Flask, request, jsonify, render_template, url_for, redirect

import datetime as dt
from werkzeug.routing import BaseConverter
from flask import send_from_directory
import logo_stuff as ls
import config as cfg
from flask_login import LoginManager, login_required

from flask_authorize import Authorize
from flask_migrate import Migrate
from config import Config


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
# включить поддержку regex
app.url_map.converters['regex'] = RegexConverter
app.config.from_object(Config)
print('start')

login = LoginManager(app)
login.init_app(app)
authorize = Authorize(app)
# from models import db
# migrate = Migrate(app, db)

@login.user_loader
def load_user(user_id):
    if User.get(user_id) or None
    return

def audio_full_path_gen(user_uid='', file_ext=u'webm', filename_prefix=u'a'):
    timestamp = dt.datetime.now().strftime("%y%m%d_%H%M%S_%f")
    return cfg.audio_folder_dash + str(filename_prefix) + u'_' + str(user_uid) + u'_' + timestamp + u'.' + str(
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


@app.route('/' + cfg.audio_folder + '/<regex("a.*\.webm"):file>')
def get_user_audio_webm(file):
    print(file)
    return send_from_directory(cfg.audio_folder_dash, file, mimetype='audio/webm')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(cfg.static, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# ключ для пользователя для страницы
@app.route('/<regex("[a-f0-9]{7}"):uid>')
def user_week_config_open(uid):
    # return u'Пользователь %s' % (uid)

    print(u'data_' + str(uid) + '.json')
    return render_template('user_week_template.html', config_path=u'data_' + str(uid) + '.json', uid=uid)


@app.route('/')
@login_required
def user_hello_server():
    return u'Сервер готов'


# секция ошибок
def error_404(e):
    # TODO включить логи 404
    return 'Ой! Такой страницы нет. Попробуйте другой адрес :)', 404


app.register_error_handler(404, error_404)


def error_500(e):
    # TODO включить логи 500
    return 'Ой! Что-то сломалось на стороне сервера. Мы уже чиним!<br/>', 500


app.register_error_handler(500, error_500)

# подключение модуля логопеда
app.register_blueprint(ls.logo_cabinet_bp)
app.register_blueprint(ls.logo_text_bp)
app.register_blueprint(ls.logo_text_post_bp)
app.register_blueprint(ls.logo_save_week_bp)
app.register_blueprint(ls.logo_save_success_bp)
app.register_blueprint(ls.logo_save_fail_bp)
app.register_blueprint(ls.logo_new_task_bp)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('/logo_cabinet')
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()


