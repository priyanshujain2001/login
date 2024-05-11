import os
import pickle
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.addons.current.action.compose',"https://www.googleapis.com/auth/gmail.addons.current.message.action","https://www.googleapis.com/auth/gmail.compose","https://www.googleapis.com/auth/gmail.modify", "https://mail.google.com/"]
def get_credentials(SCOPES = SCOPES):
    creds = None
    if os.path.exists('gmail_sevices\\token.pickle'):
        with open('gmail_sevices\\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail_services\\client_secret_85844747848-q0bb9at2po3cu4avdr1si54qk7f45ril.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('gmail_services\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds