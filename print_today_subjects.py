from googleapiclient.discovery import build
from auth import gmail_login
from datetime import datetime, timedelta
import base64
import re


def get_email_body(payload):
    def decode(data):
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    mime_type=payload.get('mimeType','')
    if mime_type=='text/plain' and 'body' in payload and 'data' in payload['body']:
        return decode(payload['body']['data'])
    if mime_type=='text/html':
        return "[html email content-not printed]"
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain' and 'body' in part and 'data' in part['body']:
                return decode(part['body']['data'])
        for part in payload['parts']:
            if part.get('mimeType') == 'text/html':
                return "[HTML email content – not printed]"

    return "(No readable text content)"

def get_gmail_service():
    creds = gmail_login()
    return build("gmail", "v1", credentials=creds)




def print_last_7_days_emails():
    service = get_gmail_service()

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y/%m/%d')
    query = f'after:{seven_days_ago}'

    response = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=10  
    ).execute()

    messages = response.get('messages', [])

    print("Emails from the last 7 days:\n")

    if not messages:
        print("No emails found.")
        return

    for i, msg in enumerate(messages, start=1):
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        headers = msg_data['payload']['headers']
        """for i in headers:
            if i['name']=='Subject':
                print(i['value'])"""

        subject = next(
            (h['value'] for h in headers if h['name'] == 'Subject'),
            '(No Subject)'
        )

        from_email = next(
            (h['value'] for h in headers if h['name'] == 'From'),
            '(Unknown Sender)'
        )
        from_email2=next(
            (h['value'] for h in headers if h['name']=='Date'),
            '(unknown date)'
        )

        body = get_email_body(msg_data['payload'])

        print(f"\n{'='*24}")
        print(f"Email {i}")
        print(f"From   : {from_email}")
        print(f"Subject: {subject}")
        print(f"date: {from_email2}")
        print(f"\n--- Message Body ---\n")
        print(body)
        print(f"{'='*24}\n")   



if __name__ == "__main__":
    print_last_7_days_emails()
    