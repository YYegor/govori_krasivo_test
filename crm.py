# -*- coding: utf-8 -*-
# 03.01.2021, created by Egor Eremenko
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import config as cfg


# example from google API
def read_paragraph_element(element):
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
def read_strucutural_elements(elements):
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
                text.append(read_paragraph_element(elem))

    return text


def get_video_data():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cfg.g_sheet_pickle_path):
        with open(cfg.g_sheet_pickle_path, 'rb') as token:
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
        with open(cfg.g_sheet_pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=cfg.clients_spreadsheet_id,
                                range=cfg.video_range_name).execute()
    values = result.get('values', [])

    return values


def get_user_crm_data():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cfg.g_sheet_pickle_path):
        with open(cfg.g_sheet_pickle_path, 'rb') as token:
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
        with open(cfg.g_sheet_pickle_path, 'wb') as token:
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


def get_text_library():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cfg.g_docs_pickle_path):
        with open(cfg.g_docs_pickle_path, 'rb') as token:
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
        with open(cfg.g_docs_pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=cfg.text_library_docs_id).execute()
    content = document.get('body').get('content')
    text_list = read_strucutural_elements(content)
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
    collection = []

    for i, line in enumerate(sound_content):
        if line == u'{\n':
            str_temp = ''
            for j, subline in enumerate(sound_content[i + 1:]):
                if subline != u'}\n':
                    str_temp += subline
                else: break
            collection.append(str_temp.replace('\n', '<br/>'))
    return collection

def get_sound_collection(sound=u'Л'):
    content = get_text_library()
    p0, p1 = text_lib_find_sound_pos(get_text_library(), sound)
    #TODO: exceptions
    return text_lib_get_s_collection(content[p0:p1])

if __name__ == '__main__':
    print (get_sound_collection(sound=u'Л'))

    exit()

    print(get_video_data())
    exit()

    clients_data = get_user_crm_data()
    c = list(clients_data.items())
    print(c)
