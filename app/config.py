"""Configuration management for the outreach application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Environment-backed settings loaded once at import time."""

    openai_api_key: str
    openai_model: str
    sender_email: str
    gmail_credentials_file: Path
    gmail_token_file: Path
    database_url: str
    outreach_subject_template: str
    followup_subject_template: str
    rate_limit_per_minute: int
    max_retries: int
    retry_backoff_seconds: float


settings = Settings(
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    sender_email=os.getenv("SENDER_EMAIL", ""),
    gmail_credentials_file=Path(os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")),
    gmail_token_file=Path(os.getenv("GMAIL_TOKEN_FILE", "token.json")),
    database_url=os.getenv("DATABASE_URL", "sqlite:///data/outreach.db"),
    outreach_subject_template=os.getenv("OUTREACH_SUBJECT_TEMPLATE", "Opportunity at {company}"),
    followup_subject_template=os.getenv("FOLLOWUP_SUBJECT_TEMPLATE", "Quick follow-up — {company}"),
    rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "20")),
    max_retries=int(os.getenv("MAX_RETRIES", "3")),
    retry_backoff_seconds=float(os.getenv("RETRY_BACKOFF_SECONDS", "1.5")),
)
