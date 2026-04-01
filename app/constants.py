"""Application-wide constants."""

from enum import Enum


class LeadStatus(str, Enum):
    """Supported lead lifecycle statuses."""

    NOT_SENT = "NOT_SENT"
    SENT = "SENT"
    FOLLOWUP_SENT = "FOLLOWUP_SENT"
    REPLIED = "REPLIED"
    INTERESTED = "INTERESTED"
    NOT_INTERESTED = "NOT_INTERESTED"
    NEUTRAL = "NEUTRAL"
    NEEDS_FOLLOWUP = "NEEDS_FOLLOWUP"
    BOUNCED = "BOUNCED"
    FAILED = "FAILED"


REPLY_CATEGORIES = {
    LeadStatus.INTERESTED.value,
    LeadStatus.NOT_INTERESTED.value,
    LeadStatus.NEUTRAL.value,
    LeadStatus.NEEDS_FOLLOWUP.value,
}

DEFAULT_GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]
