from gmail_services.get_credentials import get_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64

def f_send_Email(to, mail_subject, mail_body, sender_mail = "celestialassault00000@gmail.com"):
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    message = MIMEText(mail_body)
    message['from'] = sender_mail
    message['to'] = to
    message['subject'] = mail_subject
    message = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
        print(f'Message ID: {message["id"]}')
    except HttpError as error:
        print(f'Error: {error}')
    
    
