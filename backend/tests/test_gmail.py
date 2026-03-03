import pickle
from googleapiclient.discovery import build

with open("secrets/token.pickle", "rb") as token:
    creds = pickle.load(token)

service = build("gmail", "v1", credentials=creds)

results = service.users().messages().list(userId="me", maxResults=5).execute()
messages = results.get("messages", [])

print("Latest messages:")
for msg in messages:
    print(msg["id"])
