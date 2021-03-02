# -*- coding: utf-8 -*-
# 03.01.2021, created by Egor Eremenko
import codecs
import config as cfg
import ext_data
from flask import render_template, Blueprint, request, jsonify
from json import loads
import glob


def debug_convert_cfg_json(decoded_data):
    """
    :param decoded_data:
    :return: json с добавкой "data = '[" для чтения конфига через json+js
    """

    try:
        decoded_data = u"data = '[" + str(decoded_data) + "]';"
    except TypeError as e:
        print(u'Ошибка при склейке json и строки конфига недели')
    return decoded_data


def save_week_conf_to_file(data, filename=u'data.json'):
    r = loads(data.decode())
    client_id = r['client']
    # TODO: заменить имя файла на автоматическое
    filename = cfg.week_cfg_folder + '/' + u'data_' + str(client_id) + u'.json'

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


@logo_text_bp.route(u'/logo_text')
def get_text_data(sound='Р'):
    print(request.args)

    sound_get = ''
    try:
        sound_get = request.args.get("sound")
    except:
        pass

    if sound_get != '':
        sound = sound_get
    # print ("get_text_data", sound)
    print("get_text_data", request.args.getlist("tags[]"))

    tags_requested = []
    try:
        tags_requested = request.args.getlist("tags[]")
    except:
        pass
    tags_requested = list(set(tags_requested))
    # если библиотека загружена заново (пустые теги), то перечитать библиотеку из googledocs
    if tags_requested == []:
        text_coll = ext_data.get_sound_collection(sound, nocache=True)
    else:
        text_coll = ext_data.get_sound_collection(sound)
    # all_tags = ext_data.find_sound_collection_tags(text_coll)

    selected_lines = ext_data.find_text_by_tag(text_coll, tags_requested)

    all_tags = ext_data.find_sound_collection_tags(selected_lines)

    if len(all_tags) > 0:
        all_tags = sorted(all_tags)


    if len(tags_requested) > 0:
        tags_requested = sorted(tags_requested)

    tags_colls = ext_data.text_convert_strcoll_listcoll(selected_lines, convert_n=True)

    return render_template(u'logo_text_sugg.html', tags_selected=tags_requested, tags=all_tags, collection=tags_colls)


logo_text_post_bp = Blueprint('logo_text_post', __name__)


@logo_text_post_bp.route(u'/logo_text_post', methods=['POST'])
def get_text_data_post(sound='Л'):
    collection = ext_data.get_sound_collection(sound)

    return u'<br/><br/>'.join(collection)


logo_cabinet_bp = Blueprint('logo_cabinet', __name__, template_folder='templates')


@logo_cabinet_bp.route('/logo_cabinet')
def logo_cabinet():
    # загрузить данные клиентов

    clients_data = ext_data.get_user_crm_data()
    # TODO: exception for user

    clients_list = list(clients_data.items())

    video_list = ext_data.get_video_data()[1:]
    # TODO: exception for video
    return render_template('logo_cabinet.html', clients=clients_list, video=video_list)


# https://govorikrasivo.atlassian.net/browse/GK-9
logo_new_task_bp = Blueprint('logo_newtask', __name__)


@logo_new_task_bp.route('/logo_newtask')
def logo_new_task(client='abcdef0'):
    file_list = []
    response = ''
    # TODO: нужно убрать вызов import os из модуля
    import os

    os.chdir(cfg.audio_folder_dash)
    # TODO: второй вызов не должен ломать change dir
    print(os.getcwd())
    mask = u"*" + client + '*.webm'

    print(mask)
    for file in glob.glob(mask):
        # print (file)
        file_list.append(file)
    for file in file_list:
        response += '<audio controls src="' + cfg.audio_folder + '/' + file + '"></audio></br>'
    # print (response)
    return response


if __name__ == '__main__':
    # print(ext_data.get_video_data()[1:])

    pass
