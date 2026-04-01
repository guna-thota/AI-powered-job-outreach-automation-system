"""Gmail API client wrapper for sending and fetching messages."""

from __future__ import annotations

import base64
from email.message import EmailMessage
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.config import settings
from app.constants import DEFAULT_GMAIL_SCOPES


class GmailClient:
    """Thin wrapper for Gmail API operations used by the system."""

    def __init__(self, scopes: list[str] | None = None) -> None:
        self.scopes = scopes or DEFAULT_GMAIL_SCOPES
        self.service = build("gmail", "v1", credentials=self._load_credentials(), cache_discovery=False)

    def _load_credentials(self) -> Credentials:
        creds = None
        if settings.gmail_token_file.exists():
            creds = Credentials.from_authorized_user_file(str(settings.gmail_token_file), self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(settings.gmail_credentials_file), self.scopes
                )
                creds = flow.run_local_server(port=0)
            settings.gmail_token_file.write_text(creds.to_json(), encoding="utf-8")
        return creds

    def send_message(self, to_email: str, subject: str, body: str, thread_id: str | None = None) -> dict[str, Any]:
        """Send a plain text email and return Gmail API response."""
        message = EmailMessage()
        message["To"] = to_email
        message["From"] = settings.sender_email or "me"
        message["Subject"] = subject
        message.set_content(body)

        payload: dict[str, Any] = {
            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8"),
        }
        if thread_id:
            payload["threadId"] = thread_id
        return (
            self.service.users()
            .messages()
            .send(userId="me", body=payload)
            .execute()
        )

    def list_inbox_messages(self, query: str = "in:inbox newer_than:14d", limit: int = 50) -> list[dict[str, Any]]:
        """List inbox message metadata matching query."""
        response = self.service.users().messages().list(userId="me", q=query, maxResults=limit).execute()
        return response.get("messages", [])

    def get_message(self, message_id: str) -> dict[str, Any]:
        """Get full message payload."""
        return (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
