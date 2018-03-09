
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import sys
import Adafruit_DHT

import time

try:
    import argparse
    flags=argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
#APPLICATION_NAME = 'Google Sheets API Python Quickstart'
APPLICATION_NAME = 'DHT_IOT'



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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the Temperature and 
    Humidity data from the sensor spreadsheet:
    https://docs.google.com/spreadsheets/d/
    1Mfl3bvFG3RlKi5XFyjmNtOPHTn6oiNV4uIlzvOZEr_Y/edit#gid=0
    """
    
    #Validating Credentials
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
                    
                    
                    
    #Creating a Spreadsheet Service 
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1Mfl3bvFG3RlKi5XFyjmNtOPHTn6oiNV4uIlzvOZEr_Y'
    rangeName = 'IOT_DHT_Sensor!A:B'
    print("Now Accessing data from dht11 sensor and uploading \
    it onto a Google Spreadsheet on Cloud")
    
    
    values = [
         [
            # Cell values ...
            "Humidity","Temperature"
         ],
         # Additional rows ...
    ]
    body = {
       'values': values
    }
    
    #Uploading the Column Names onto the spreadsheet.
    result = service.spreadsheets().values().append(
      spreadsheetId=spreadsheetId, range=rangeName,
       valueInputOption="USER_ENTERED", body=body).execute()
    i=1
    while True:
      #Comment the next 2 lines, if you want to run it continuously.
      if i == 15:
         break
         
         
      #Collectng Data from sensor after every 3 seconds.
      time.sleep(3) 
      
      
      # Extracting the Temperature and Humidity from DHT Sensor.
      humidity, temperature = Adafruit_DHT.read_retry(11,4)
      temp = temperature
      hum = humidity
      i = i+1
      
      
      #Storing data into a JSON object
      values = [
         [
            # Cell values ...
            hum,temp
         ],
         # Additional rows here...
      ]
      body = {
         'values': values
      }
      
      
      #Uploading the data onto the spreadsheet on the cloud
      result = service.spreadsheets().values().append(
      spreadsheetId=spreadsheetId, range=rangeName,
       valueInputOption="USER_ENTERED", body=body).execute()



    #Extracting data from the smae spreadsheet.
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])



    #Printing the data from the Spreadsheet on the cloud.
    print("Now getting data from the Google Spreadsheet.")
    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A and B, which correspond to indices 0 and 1.
            print('%s, %s' % (row[0], row[1]))


if __name__ == '__main__':
    main()
