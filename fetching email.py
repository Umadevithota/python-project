
import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
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
    return creds

def fetch_emails(user_id='me', label_id='INBOX', max_results=5):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    try:
        response = service.users().messages().list(userId=user_id, labelIds=[label_id], maxResults=max_results).execute()
        messages = response.get('messages', [])
        
        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            subject = ''
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
            
            # Process the email subject and body as needed
            print(f"Subject: {subject}\nBody: {body}\n{'-'*30}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    fetch_emails()
