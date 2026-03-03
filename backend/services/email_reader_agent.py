import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service(token_path="secrets/token.json"):

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    return build("gmail", "v1", credentials=creds)


def read_latest_emails(limit=5):

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=limit
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        txt = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        payload = txt["payload"]
        headers = payload["headers"]

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]

            if h["name"] == "From":
                sender = h["value"]

        emails.append({
            "subject": subject,
            "from": sender
        })

    return emails
EOF