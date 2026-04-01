"""Follow-up scheduling logic."""

from __future__ import annotations

from datetime import datetime, timedelta

from app.constants import LeadStatus
from app.database import crud
from app.database.db import get_session
from app.email.email_service import EmailService
from app.utils.logger import get_logger

logger = get_logger(__name__)


def should_send_followup(last_sent_date: datetime | None, days: int = 3) -> bool:
    """Return True when enough time has passed for a follow-up."""
    if not last_sent_date:
        return False
    return datetime.utcnow() - last_sent_date >= timedelta(days=days)


def run_followup_job() -> None:
    """Send follow-ups to leads with no reply after threshold window."""
    service = EmailService()
    with get_session() as session:
        leads = crud.list_leads(session)

    for lead in leads:
        if lead.status in {
            LeadStatus.SENT.value,
            LeadStatus.NEUTRAL.value,
            LeadStatus.NEEDS_FOLLOWUP.value,
        } and should_send_followup(lead.last_email_sent_at):
            logger.info("Sending follow-up to %s", lead.email)
            service.send_followup_email(lead)
