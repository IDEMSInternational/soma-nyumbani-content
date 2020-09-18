from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# Export a google doc to local pdf
# Code based on: https://developers.google.com/drive/api/v3/quickstart/python

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly'] 

def gdoc_to_pdf(doc_id, out_filename): 
    drive_service = login()
    download_doc(drive_service, doc_id, out_filename)


def login():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def download_doc(drive_service, doc_id, out_filename):
    request = drive_service.files().export_media(fileId=doc_id,
                                                mimeType='application/pdf')
    fh = io.FileIO('outputs/'+ out_filename +'.pdf','w+b')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

# Test script if running directly
if __name__ == '__main__':
    main('1tP9jDMBg3KiyvCOkXYbGRr-jyKvTO5vZkLLM7zMUbpY','a-to-z-workout')
    
