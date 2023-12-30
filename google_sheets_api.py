from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

class GoogleSheets():
    def __init__(self,service=None):
        self.service = service
            # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo'
        SAMPLE_RANGE_NAME = 'Entrys!A2:D4'
        
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('sheets', 'v4', credentials=creds)
        except HttpError as err:
            print(err)

    def input_entry(self, value, category, comments):
        try:
            body = {
                'values': [[value, category, comments, datetime.now().strftime('%d/%m/%Y, %H:%M:%S')]]
            }
            result = self.service.spreadsheets().values().append(
                spreadsheetId='1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo', range='inflows!A2:D',
                valueInputOption='USER_ENTERED', body=body).execute()

            print(f"Entry inserted: {value}, {category}, {comments}")
            return result
        except HttpError as error:
            print(f"An error occurred in input_entry: {error}")
            return error
        

    def input_outs(self, value, classification, type, comments):
        try:
            body = {
                'values': [[value, classification, type, comments, datetime.now().strftime('%d/%m/%Y, %H:%M:%S')]]
            }
            result = self.service.spreadsheets().values().append(
                spreadsheetId='1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo', range='outflows!A2:E',
                valueInputOption='USER_ENTERED', body=body).execute()

            print(f"Outflow inserted: {value}, {classification}, {type}, {comments}")
            return result
        except HttpError as error:
            print(f"An error occurred in input_outs: {error}")
            return error
        

    def input_transfers(self, value, origin, destine, coments):
        try:
            body = {
                'values': [[value, origin, destine, coments, datetime.now().strftime('%d/%m/%Y, %H:%M:%S')]]
            }
            result = self.service.spreadsheets().values().append(
                spreadsheetId='1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo', range='transfers!A2:E2',
                valueInputOption='USER_ENTERED', body=body).execute()
            
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
        
    def show_report(self, column): 
        try:
            sheet = self.service.spreadsheets()
            if column == 'Total Entrys':
                result = sheet.values().get(spreadsheetId='1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo',range='reports!A2:A').execute()
                values = result.get('values', [])
                print(values) # If you want more values, change the range or way you access the value below
                print(values[0][0])
                return values[0][0]
                
            elif column == 'Total Outs':
                result = sheet.values().get(spreadsheetId='1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo',range='reports!B2:B').execute()
                values = result.get('values', [])
                print(values) # If you want more values, change the range or way you access the value below
                print(values[0][0])
                return values[0][0]
            
            elif column == 'Total Transfers':
                result = sheet.values().get(spreadsheetId='1n8WV4Ccw8hxPDSJ64hSRTIWRRuNz148H52ZWLbAEhfo',range='reports!C2:C').execute()
                values = result.get('values', [])
                print(values) # If you want more values, change the range or way you access the value below
                print(values[0][0])
                return values[0][0]

        except Exception as error:
            print(error)

 #google_sheets_api = GoogleSheets()
# #google_sheets_api.input_entry(100,'investments','facebook stock dividends')
# # google_sheets_api.input_outs(500,'fixed','cash','car repairs')
# # google_sheets_api.input_transfers(2000,'account 1','account 2','donation')
# # google_sheets_api.display_report('Total Entry')
# # google_sheets_api.display_report('Total Outs')
# # google_sheets_api.display_report('Total Transfers')
