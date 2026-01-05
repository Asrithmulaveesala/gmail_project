from gmail_service import get_gmail_service
from datetime import datetime

def print_today_email_subjects():
    service = get_gmail_service()

    today = datetime.now().strftime('%Y/%m/%d')
    query = f'after:{today}'

    response = service.users().messages().list(
        userId='me',
        q=query
    ).execute()

    messages = response.get('messages', [])

    print("\n📧 Subjects of today's emails:\n")

    if not messages:
        print("No emails received today.")
        return

    for i, msg in enumerate(messages, start=1):
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Subject']
        ).execute()

        headers = msg_data['payload']['headers']
        subject = next(
            (h['value'] for h in headers if h['name'] == 'Subject'),
            '(No Subject)'
        )

        print(f"{i}. {subject}")

if __name__ == "__main__":
    print_today_email_subjects()
