# -*- coding: utf-8 -*-
# 03.01.2021, created by Egor Eremenko
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import config as cfg
from  functools import lru_cache

# example from google API
def text_read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    # print (type(text_run), text_run)
    if not text_run:
        return ''
    return text_run.get('content')


# example from google API
def text_read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = []
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text.append(text_read_paragraph_element(elem))

    return text


def get_video_data():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cfg.g_sheet_pickle_readonly_path):
        with open(cfg.g_sheet_pickle_readonly_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cfg.g_sheet_creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cfg.g_sheet_pickle_readonly_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=cfg.clients_spreadsheet_id,
                                range=cfg.video_range_name).execute()
    values = result.get('values', [])

    return values

# def get_user_records():
#     # If modifying these scopes, delete the file token.pickle.
#     SCOPES = cfg.g_scope_sheets_read_only
#
#
#
#     creds = None
#
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists(cfg.g_sheet_pickle_readonly_path):
#         with open(cfg.g_sheet_pickle_readonly_path, 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 cfg.g_sheet_creds_path, SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open(cfg.g_sheet_pickle_readonly_path, 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('sheets', 'v4', credentials=creds)
#
#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=cfg.clients_spreadsheet_id,
#                                 range=cfg.clients_range_name).execute()
#     values = result.get('values', [])
#
#     clients = {}
#
#     if not values:
#         print('Clients: No data found.')
#     else:
#
#         for rows in values[1:]:
#             clients[rows[0]] = rows[1]
#         # print(clients)
#
#         return clients


def get_user_crm_data():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = cfg.g_scope_sheets_read_only

    # The ID and range of a sample spreadsheet.

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cfg.g_sheet_pickle_readonly_path):
        with open(cfg.g_sheet_pickle_readonly_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cfg.g_sheet_creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cfg.g_sheet_pickle_readonly_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=cfg.clients_spreadsheet_id,
                                range=cfg.clients_range_name).execute()
    values = result.get('values', [])

    clients = {}
    if not values:
        print('Clients: No data found.')

    else:
        # print(values)


        for rows in values[1:]:
            clients[rows[0]] = rows[1]
        # print(clients)

    return clients


def get_text_library():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = cfg.g_scope_docs_read_only

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    text_list = []
    if os.path.exists(cfg.g_docs_pickle_readonly_path):
        with open(cfg.g_docs_pickle_readonly_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cfg.g_docs_creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cfg.g_docs_pickle_readonly_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    try:
        document = service.documents().get(documentId=cfg.text_library_docs_id).execute()
    except:
        print("get_text_library failed")
        return text_list

    content = document.get('body').get('content')
    text_list = text_read_strucutural_elements(content)

    return text_list



def text_lib_find_sound_pos(text_list: list, sound: str):
    '''
    найти все позиции знака "=", то есть границ текста на определенную букву
    :param sound
    :param text_list
    :return: tuple
    '''
    pos_start = 0
    pos_end = len(text_list) - 1
    for i, line in enumerate(text_list):

        if line.find(u'=' + sound + '=') >= 0:
            pos_start = i + 1
        if i > pos_start and line[0] == '=':
            pos_end = i
            break

    return (pos_start, pos_end)


def text_lib_get_s_collection(sound_content: list):
    """

    :param sound_content:
    :return: list of lines
    """
    collection = []

    for i, line in enumerate(sound_content):
        if line == u'{\n':
            str_temp = ''
            for j, subline in enumerate(sound_content[i + 1:]):
                if subline != u'}\n':
                    str_temp += subline
                else: break
            #collection.append(str_temp.replace('\n', '<br />'))
            collection.append(str_temp)
    return collection

@lru_cache(maxsize=16)
def get_sound_collection(sound=u'Л'):
    content = []
    content = get_text_library()

    return_list = []
    p0 = None
    p1 = None

    if content != []:
        try:
            p0, p1 = text_lib_find_sound_pos(content, sound)
        except:
            print (' get_sound_collection text_lib_find_sound_pos returned problem')

    if p0 is not None and p1 is not None:
        try:
            return_list = text_lib_get_s_collection(content[p0:p1])
        except:
            print('get_sound_collection text_lib_get_s_collection returned problem')

    return return_list


#https://govorikrasivo.atlassian.net/browse/GK-7
def find_sound_collection_tags(text_lib_get_s_collection:list, sound='Р'):
    lines = text_lib_get_s_collection
    #найти все теги, заключенные в []
    return list(set(extract_tags(lines)))


#https://govorikrasivo.atlassian.net/browse/GK-7
def extract_tags(lines):
    tags = []

    for line in lines:
        #print('extract_tags loop', line)

        endl = line.rfind(']')
        line = line[1:endl]
        line = line.replace(']', '')

        line_list = line.split('[')
        line_list = [item.strip() for item in line_list]

        tags.extend(line_list)
    tags = list(set(tags))
    return tags


#https://govorikrasivo.atlassian.net/browse/GK-7
def find_text_by_tag(text_lib_get_s_collection:list, tags_set:list):
    resulting_texts = []
    for line in text_lib_get_s_collection:
        tags = extract_tags([line])
        #print ('line ', line)
        #print ('tags ', tags)

        #TODO CONTINUE. нужно находить тексты без тегов,

        #перечечение сетов дает сет размера tags_set, то есть в текущей линии нашлись оба тега
        if len(list(set(tags) & set(tags_set))) == len(tags_set):
            resulting_texts.append(line)
    return resulting_texts

#https://govorikrasivo.atlassian.net/browse/GK-7
def text_convert_strcoll_listcoll(collection:list, convert_n=False):
    tags_n_lines = []
    for coll in collection:

        tags = extract_tags([coll])
        pure_line = coll[str(coll).find('\n')+1:]
        if convert_n == True:
            pure_line = pure_line.replace('\n', '<br />')
        #print (pure_line)
        tags_n_lines.append((tags, pure_line))

    return tags_n_lines


def get_new_audio():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cfg.g_sheet_pickle_readonly_path):
        with open(cfg.g_sheet_pickle_readonly_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cfg.g_sheet_creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cfg.g_sheet_pickle_readonly_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=cfg.clients_spreadsheet_id,
                                range=cfg.clients_range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        # print(values)
        clients = {}

        for rows in values[1:]:
            clients[rows[0]] = rows[1]
        # print(clients)

        return clients


if __name__ == '__main__':
    print(sorted(['сложно', 'д/з']))

    coll = get_sound_collection(sound="Р")
    print(extract_tags(coll))

    selected_lines = find_text_by_tag(coll, ['д/з','сложно'])

    all_tags = find_sound_collection_tags(selected_lines)

    print(text_convert_strcoll_listcoll(selected_lines, convert_n=True))
    #print (all_tags)

    exit()

    print(get_video_data())
    exit()

    clients_data = get_user_crm_data()
    c = list(clients_data.items())
    print(c)
