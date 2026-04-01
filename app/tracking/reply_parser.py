"""Inbox synchronization and reply extraction logic."""

from __future__ import annotations

from typing import Any

from app.email.gmail_client import GmailClient


class ReplyParser:
    """Extract reply snippets and metadata from Gmail inbox."""

    def __init__(self) -> None:
        self.gmail_client = GmailClient()

    @staticmethod
    def _header_value(payload: dict[str, Any], header_name: str) -> str | None:
        headers = payload.get("headers", [])
        for header in headers:
            if header.get("name", "").lower() == header_name.lower():
                return header.get("value")
        return None

    def fetch_reply_candidates(self, limit: int = 50) -> list[dict[str, str]]:
        """Get potential reply messages from inbox."""
        candidates = []
        for meta in self.gmail_client.list_inbox_messages(limit=limit):
            message = self.gmail_client.get_message(meta["id"])
            payload = message.get("payload", {})
            candidates.append(
                {
                    "message_id": message.get("id", ""),
                    "thread_id": message.get("threadId", ""),
                    "from": self._header_value(payload, "From") or "",
                    "subject": self._header_value(payload, "Subject") or "",
                    "snippet": message.get("snippet", ""),
                }
            )
        return candidates
