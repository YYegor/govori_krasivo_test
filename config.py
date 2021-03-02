# -*- coding: utf-8 -*-
# 03.01.2021, created by Egor Eremenko
import os

DEBUG = True


static = os.path.join('static')
audio_folder = u'user_content_audio'
audio_folder_dash = os.path.join(audio_folder, u'')
week_cfg_folder = os.path.join(u'static', u'weeks')


# crm on google sheets
g_scope_docs_read_only = ['https://www.googleapis.com/auth/documents.readonly']
g_scope_sheets_read_only = ['https://www.googleapis.com/auth/spreadsheets.readonly']
clients_spreadsheet_id = u'1Cn4X8htkVz_EzFjBo7lWI0FtGHxWI4m1GUyoi1vhap4'
text_library_docs_id = u'1OhSalTTCOpZ-mlhEGGPlfRMMEdtOBLdq4hxayMhqXpo'
clients_range_name = u'clients!A1:G7'
video_range_name = u'video!A1:E100'
g_sheet_creds_path = os.path.join(u'secret', u'credentials.json')
g_sheet_pickle_readonly_path = os.path.join(u'secret', u'token.pickle')
g_docs_creds_path = os.path.join(u'secret', u'credentials_docs.json')
g_docs_pickle_readonly_path = os.path.join(u'secret', u'token_docs.pickle')

if __name__ == '__main__':
    print(audio_folder_dash)
    print(week_cfg_folder)
