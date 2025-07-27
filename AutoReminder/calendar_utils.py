from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def _get_service():
    """Authenticate (OAuth) and return an authorised Calendar API service."""
    creds: Credentials | None = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "Google OAuth client secret 'credentials.json' is missing."
                )
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(event: Dict) -> str:
    """Insert an event into the user's primary calendar and return its HTML link."""
    if not event.get("datetime"):
        raise ValueError("No datetime found in parsed event; cannot create calendar entry.")

    service = _get_service()

    start: datetime = event["datetime"]
    end = start + timedelta(minutes=30)

    body = {
        "summary": event.get("title", "Reminder"),
        "description": event.get("link", "") or event.get("raw", ""),
        "start": {"dateTime": start.isoformat()},
        "end": {"dateTime": end.isoformat()},
    }

    created = service.events().insert(calendarId="primary", body=body).execute()
    return created.get("htmlLink", "")