"""Reusable campaign metrics engine."""

from __future__ import annotations

from app.constants import LeadStatus
from app.database.models import Lead


def calculate_metrics(leads: list[Lead]) -> dict[str, float]:
    """Compute outreach KPIs from lead statuses."""
    total = len(leads)
    sent = sum(1 for lead in leads if lead.status in {LeadStatus.SENT.value, LeadStatus.FOLLOWUP_SENT.value, LeadStatus.REPLIED.value, LeadStatus.INTERESTED.value, LeadStatus.NOT_INTERESTED.value, LeadStatus.NEUTRAL.value, LeadStatus.NEEDS_FOLLOWUP.value})
    replies = sum(1 for lead in leads if lead.status in {LeadStatus.REPLIED.value, LeadStatus.INTERESTED.value, LeadStatus.NOT_INTERESTED.value, LeadStatus.NEUTRAL.value, LeadStatus.NEEDS_FOLLOWUP.value})
    interested = sum(1 for lead in leads if lead.status == LeadStatus.INTERESTED.value)
    followups = sum(1 for lead in leads if lead.status == LeadStatus.FOLLOWUP_SENT.value)
    followup_reply = sum(1 for lead in leads if lead.status in {LeadStatus.INTERESTED.value, LeadStatus.NOT_INTERESTED.value, LeadStatus.NEUTRAL.value, LeadStatus.NEEDS_FOLLOWUP.value} and lead.last_email_sent_at is not None)

    response_rate = (replies / sent * 100) if sent else 0.0
    conversion_rate = (interested / sent * 100) if sent else 0.0
    followup_effectiveness = (followup_reply / followups * 100) if followups else 0.0

    return {
        "total_leads": float(total),
        "emails_sent": float(sent),
        "replies": float(replies),
        "interested": float(interested),
        "response_rate": response_rate,
        "conversion_rate": conversion_rate,
        "followup_effectiveness": followup_effectiveness,
    }
