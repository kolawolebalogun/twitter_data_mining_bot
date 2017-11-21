from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import constants

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(constants.GOOGLE_CLIENT_SECRET_FILE, constants.GOOGLE_SCOPES)
        flow.user_agent = constants.GOOGLE_APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def insert_row(values):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = constants.GOOGLE_DISCOVERY_URL
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    spreadsheet_id = constants.GOOGLE_SPREAD_SHEET_ID
    range_name = constants.GOOGLE_SPREAD_SHEET_RANGE
    body = {
        u'values': [values]
    }
    value_input_option = 'RAW'
    insert_data_option = 'INSERT_ROWS'

    result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_name, body=body,
                                                    valueInputOption=value_input_option,
                                                    insertDataOption=insert_data_option).execute()
    return result
