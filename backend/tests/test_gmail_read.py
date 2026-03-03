import pickle
import base64
from googleapiclient.discovery import build

with open("secrets/token.pickle", "rb") as token:
    creds = pickle.load(token)

service = build("gmail", "v1", credentials=creds)

results = service.users().messages().list(
    userId="me",
    maxResults=5
).execute()

messages = results.get("messages", [])

print("\n📬 Latest Emails:\n")

for msg in messages:
    message = service.users().messages().get(
        userId="me",
        id=msg["id"],
        format="metadata",
        metadataHeaders=["Subject", "From", "Date"]
    ).execute()

    headers = message["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
    date = next((h["value"] for h in headers if h["name"] == "Date"), "Unknown")

    print(f"From: {sender}")
    print(f"Subject: {subject}")
    print(f"Date: {date}")
    print("-" * 50)
