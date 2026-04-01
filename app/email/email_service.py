"""Outreach email orchestration service."""

from __future__ import annotations

from app.config import settings
from app.constants import LeadStatus
from app.database import crud
from app.database.db import get_session
from app.database.models import Lead
from app.email.gmail_client import GmailClient
from app.personalization.llm_engine import LLMEngine
from app.utils.helpers import load_jinja_template
from app.utils.logger import get_logger
from app.utils.resilience import RateLimiter, retry

logger = get_logger(__name__)


class EmailService:
    """Main service that composes and sends campaign emails."""

    def __init__(self) -> None:
        self.gmail_client = GmailClient()
        self.llm_engine = LLMEngine()
        self.rate_limiter = RateLimiter(max_calls=settings.rate_limit_per_minute)
        self.cold_template = load_jinja_template("app/email/templates/cold_email.txt")
        self.followup_template = load_jinja_template("app/email/templates/followup_email.txt")

    def send_cold_email(self, lead: Lead) -> None:
        """Generate personalization and send first-touch message."""
        personalized_line = retry(
            lambda: self.llm_engine.generate_personalized_line(
                name=lead.name,
                company=lead.company,
                role=lead.role,
                tier=lead.tier,
            ),
            max_attempts=settings.max_retries,
            backoff_seconds=settings.retry_backoff_seconds,
        )
        subject = settings.outreach_subject_template.format(company=lead.company)
        body = self.cold_template.render(
            name=lead.name,
            company=lead.company,
            role=lead.role,
            personalized_line=personalized_line,
            sender_email=settings.sender_email,
        )
        self._send_and_track(lead, subject, body, LeadStatus.SENT.value, "COLD_EMAIL")

    def send_followup_email(self, lead: Lead) -> None:
        """Send follow-up email using thread id if available."""
        subject = settings.followup_subject_template.format(company=lead.company)
        body = self.followup_template.render(
            name=lead.name,
            company=lead.company,
            role=lead.role,
            sender_email=settings.sender_email,
        )
        self._send_and_track(lead, subject, body, LeadStatus.FOLLOWUP_SENT.value, "FOLLOWUP")

    def _send_and_track(self, lead: Lead, subject: str, body: str, lead_status: str, event_type: str) -> None:
        self.rate_limiter.wait_for_slot()

        def do_send():
            return self.gmail_client.send_message(
                to_email=lead.email,
                subject=subject,
                body=body,
                thread_id=lead.thread_id,
            )

        try:
            result = retry(do_send, settings.max_retries, settings.retry_backoff_seconds)
            with get_session() as session:
                crud.update_lead_status(
                    session,
                    lead.email,
                    status=lead_status,
                    thread_id=result.get("threadId"),
                )
                crud.log_email_event(
                    session,
                    lead_email=lead.email,
                    event_type=event_type,
                    status="SUCCESS",
                    subject=subject,
                    gmail_message_id=result.get("id"),
                    metadata=result,
                )
            logger.info("Email sent to %s (%s)", lead.email, event_type)
        except Exception as exc:  # noqa: BLE001
            with get_session() as session:
                crud.update_lead_status(session, lead.email, status=LeadStatus.FAILED.value)
                crud.log_email_event(
                    session,
                    lead_email=lead.email,
                    event_type=event_type,
                    status="FAILED",
                    subject=subject,
                    metadata={"error": str(exc)},
                )
            logger.exception("Failed to send email to %s", lead.email)
