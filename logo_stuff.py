# -*- coding: utf-8 -*-
# 03.01.2021, created by Egor Eremenko
import codecs
import config as cfg
import crm
from flask import render_template, Blueprint, request, jsonify
from json import loads, dumps


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


def save_week_conf_to_file(data, filename=u'data.json'):
    r = loads(data.decode())
    client_id = r['client']
    # TODO: заменить имя файла на автоматическое
    filename = cfg.week_cfg_folder + '\\' + u'data_' + str(client_id) + u'.json'

    if cfg.DEBUG:
        print(filename, 'file will be saved')
    try:
        f = codecs.open(filename, 'w+', encoding='utf8')
    except OSError as e:
        print(' can''t open file ', filename)
        return False

    if cfg.DEBUG:
        print('save_week_conf_to_file data:', data)
    try:
        data = data.decode('utf-8')
    except UnicodeError:
        print(u'Ошибка unicode при конвертации')
        f.close()
        return False

    try:
        if cfg.DEBUG:
            f.write(debug_convert_cfg_json(data))
        else:
            f.write(data)
    except OSError:
        print(u' can''t write to file ', filename)
        return False
    finally:
        f.close()

    return True

logo_save_success_bp = Blueprint('config_success', __name__)
@logo_save_success_bp.route('/configsuccess')
def logo_config_success():
    return u'Файл урока принят и сохранён.'

logo_save_fail_bp = Blueprint('config_fail', __name__)
@logo_save_fail_bp.route('/configfail')
def logo_config_fail():
    return u'Файл урока не был сохранён из-за ошибки.'


logo_save_week_bp = Blueprint('save_week', __name__)
@logo_save_week_bp.route('/save_week', methods=['POST'])
def logo_config_save():
    if save_week_conf_to_file(request.data):
        return jsonify({"redirect": "/configsuccess"})
    else:
        return jsonify({"redirect": "/configfail"})


logo_text_bp = Blueprint('logo_text', __name__)
@logo_text_bp.route('/logo_text')
def get_text_data(sound='Л'):
    collection = crm.get_sound_collection(sound)

    return u'<br/><br/>'.join(collection)

logo_cabinet_bp = Blueprint('logo_cabinet', __name__, template_folder='templates')
@logo_cabinet_bp.route('/logo_cabinet')
def logo_cabinet():
    # загрузить данные клиентов

    clients_list = []
    clients_data = crm.get_user_crm_data()
    # TODO: exception for user
    clients_list = list(clients_data.items())

    video_list = []
    video_list = crm.get_video_data()[1:]
    # TODO: expection for video
    return render_template('logo_cabinet.html', clients=clients_list, video=video_list)


if __name__ == '__main__':
    pass
