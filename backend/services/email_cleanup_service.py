import os
import pickle
import base64
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmailCleanupService:
    def __init__(self):
        with open("secrets/token.pickle", "rb") as token:
            creds = pickle.load(token)
        self.service = build("gmail", "v1", credentials=creds)
        self.whitelist = [
            "bell.ca", "bellmobility.com", "no-reply@bell.ca",
            "stripe.com", "notifications@stripe.com",
            "noreply@uber.com", "receipts@uber.com",
            # Add more billers here
        ]

    def get_email_details(self, msg_id):
        msg = self.service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown").lower()

        body = ""
        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                    break
        else:
            if msg["payload"]["body"].get("data"):
                body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode("utf-8", errors="ignore")

        return subject, sender, body[:2000]

    def classify(self, subject, sender, body):
        prompt = f"""Analyze this email carefully.
From: {sender}
Subject: {subject}
Body excerpt: {body[:1500]}

Classify as: Important, Bill, Lead, Personal, Marketing, Spam, Newsletter
Output ONLY JSON:
{{
  "category": "one of above",
  "confidence": 0-100,
  "due_date": "YYYY-MM-DD or null",
  "suggested_action": "AutoTrash" | "AutoKeep" | "AskUser"
}}

Rules:
- AutoTrash: Clear promo, marketing, newsletter, spam (high conf only)
- AutoKeep: Bills, payments, leads, personal (esp if whitelisted or Bill category)
- AskUser: Ambiguous advertised/lead or low conf promo
- Never AutoTrash bills or whitelisted senders
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"category": "Unknown", "confidence": 0, "due_date": None, "suggested_action": "Review"}

    def clean_inbox(self, max_emails=500):
        """Clean unread emails - call this from the brain"""
        print("Starting inbox cleanup...")

        results = self.service.users().messages().list(
            userId="me",
            q="is:unread",
            maxResults=max_emails
        ).execute()

        messages = results.get("messages", [])
        print(f"Found {len(messages)} unread emails")

        for i, msg in enumerate(messages, 1):
            subject, sender, body = self.get_email_details(msg["id"])
            analysis = self.classify(subject, sender, body)

            if (analysis["category"] in ["Marketing", "Spam", "Newsletter"] and 
                analysis["confidence"] >= 85 and 
                not any(ws in sender for ws in self.whitelist)):

                self.service.users().messages().trash(userId="me", id=msg["id"]).execute()
                print(f"Trashed: {subject}")

            elif analysis["category"] == "Bill" or any(ws in sender for ws in self.whitelist):
                self.service.users().messages().modify(
                    userId="me", id=msg["id"], body={"removeLabelIds": ["UNREAD"]}
                ).execute()
                print(f"Kept bill/receipt: {subject}")
                if analysis["due_date"] and analysis["due_date"] != "null":
                    print(f"Reminder → Pay by {analysis['due_date']}")

        print(f"Cleanup finished ({len(messages)} emails processed)")
        return len(messages)
