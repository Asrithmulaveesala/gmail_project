from googleapiclient.discovery import build
from auth import gmail_login

def get_gmail_service():
    creds = gmail_login()
    return build("gmail", "v1", credentials=creds)
