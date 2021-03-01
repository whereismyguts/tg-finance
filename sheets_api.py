from __future__ import print_function
import pickle
import os.path
import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from settings import SPREADSHEET_ID

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

cols_by_week_number = {
    1: 'L{}:M{}',
    2: 'N{}:O{}',
    3: 'P{}:Q{}',
    4: 'R{}:S{}',
}

LIST_NAME = 'фев'

def find_emtpy_cell_range(sheet):

    week = get_week_number(datetime.datetime.utcnow())
    rage_name_str = cols_by_week_number.get(week)
    values =  _get_data(sheet, LIST_NAME + '!' + rage_name_str.format(1,300))
    return LIST_NAME + '!' + rage_name_str.format(len(values)+1, len(values)+1)
    

def get_service_from_doc():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def append_transaction(text, value):
    service = get_service_from_doc()
    sheet = service.spreadsheets()
    
    range_name = find_emtpy_cell_range(sheet)
    set_data(service, range_name, [text, value])

def get_data_from_current_list(range_name):
    service = get_service_from_doc()
    sheet = service.spreadsheets()
    return _get_data(sheet, LIST_NAME + '!' + range_name)

def _get_data(sheet, range_name):
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()
    return result.get('values', [None])

def set_data(service, range_name, values):
    body = {'values': [values]}
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='RAW', 
        body=body
    ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def get_week_number(dt):
    if dt.day < 10:
        start = (dt - datetime.timedelta(days=10)).replace(day=10)
        # end = dt.replace(day=9)
    else:
        start = dt.replace(day=10)
        # end = (dt.replace(day=27) + datetime.timedelta(10)).replace(day=9)
    delta = 7
    for i in range(1,5):
        if dt < start + datetime.timedelta(days=delta*i):
            return i


def test_dates():
    for d in [
        datetime.datetime(2021, 1, 15),
        datetime.datetime(2021, 1, 30),
        datetime.datetime(2021, 2, 5),
        datetime.datetime(2021, 2, 13),
        datetime.datetime(2021, 3, 5),
        datetime.datetime(2021, 3, 11),
    ]:
      
        print(str(d))
        print(get_week_number(d))
        print('--')


if __name__ == '__main__':
    append_transaction('test1', 50)
    # append_transaction('test2', 350)
    # append_transaction('test3', 200)
    # test_dates()