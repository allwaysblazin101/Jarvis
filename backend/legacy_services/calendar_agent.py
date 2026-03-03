from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def get_calendar_service():

    creds = Credentials.from_authorized_user_file(
        "secrets/token.json",
        ["https://www.googleapis.com/auth/calendar"]
    )

    return build("calendar", "v3", credentials=creds)


def list_upcoming_events():

    service = get_calendar_service()

    events = service.events().list(
        calendarId="primary",
        maxResults=10,
        orderBy="startTime",
        singleEvents=True
    ).execute()

    return events.get("items", [])
EOF