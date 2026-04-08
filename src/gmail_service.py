import os
import pickle
import base64
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from utils.logger import logger

# SCOPES define what the Agent is allowed to do.
# 'gmail.modify' allows us to read, draft, and mark emails as read.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Authenticates the user and returns the Gmail API service object."""
    creds = None

    # 1. Check if we already have a saved login (token.pickle)
    if os.path.exists('token.pickle'):
        logger.info("Found saved credentials in token.pickle")
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # 2. If there are no valid credentials, we need to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            logger.info("No valid credentials found. Starting new login flow...")
            if not os.path.exists('credentials.json'):
                logger.error("CRITICAL: credentials.json not found in root folder!")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # 3. Save the credentials for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            logger.info("Credentials saved to token.pickle")

    # 4. Build the official Gmail Service
    service = build('gmail', 'v1', credentials=creds)
    logger.info("Gmail Service successfully built and ready to use.")
    return service

def fetch_unread_emails(service):
    """Fetches a list of unread message IDs from the inbox."""
    try:
        # Search for 'is:unread' to only get new emails
        result = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = result.get('messages', [])

        if not messages:
            logger.info("No unread emails found.")
            return []
        
        logger.info(f"Found {len(messages)} unread email(s).")
        return messages
    except Exception as e:
        logger.error(f"An error occurred while fetching emails: {e}")
        return []

def get_email_details(service, msg_id):
    """Gets the snippet (brief summary) of a specific email by ID."""
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
        snippet = message.get('snippet', '')
        logger.info(f"Fetched details for email ID: {msg_id}")
        return snippet
    except Exception as e:
        logger.error(f"Error fetching details for {msg_id}: {e}")
        return None

def create_gmail_draft(service, body_content, original_msg_id):
    """Creates a draft reply in Gmail linked to the original email."""
    try:
        # 1. Get the original message to find the sender and subject
        original = service.users().messages().get(userId='me', id=original_msg_id).execute()
        headers = original.get('payload', {}).get('headers', [])
        
        # Find the 'From' and 'Subject' headers
        to_email = next(h['value'] for h in headers if h['name'] == 'From')
        subject = next(h['value'] for h in headers if h['name'] == 'Subject')

        # 2. Build the Email Object
        message = EmailMessage()
        message.set_content(body_content)
        message['To'] = to_email
        message['From'] = 'me'
        message['Subject'] = f"Re: {subject}"
        
        # 3. Encode the message to Base64 (Required by Gmail API)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}
        
        # 4. Create the draft in the user's Gmail
        draft = service.users().drafts().create(userId='me', body=create_message).execute()
        logger.info(f"Draft created successfully! Draft ID: {draft['id']}")
        return draft
        
    except Exception as e:
        logger.error(f"Failed to create draft: {e}")
        return None

if __name__ == "__main__":
    # Test the connection and fetch
    svc = get_gmail_service()
    if svc:
        fetch_unread_emails(svc)