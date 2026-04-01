"""Pipeline coordinator: Gmail → parser → classifier → DB update → metrics."""

from __future__ import annotations

from app.constants import LeadStatus
from app.database import crud
from app.database.db import get_session
from app.tracking.classifier import ReplyClassifier
from app.tracking.metrics import calculate_metrics
from app.tracking.reply_parser import ReplyParser
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TrackingPipeline:
    """Synchronizes inbox replies and updates campaign intelligence."""

    def __init__(self) -> None:
        self.reply_parser = ReplyParser()
        self.classifier = ReplyClassifier()

    def sync_replies(self) -> dict[str, float]:
        """Process replies and return updated metrics."""
        candidates = self.reply_parser.fetch_reply_candidates()
        logger.info("Fetched %s inbox candidates", len(candidates))

        with get_session() as session:
            leads = {lead.email.lower(): lead for lead in crud.list_leads(session)}
            for message in candidates:
                sender = message["from"].lower()
                matching = next((email for email in leads if email in sender), None)
                if not matching:
                    continue
                category = self.classifier.classify(message["snippet"])
                status = category if category in {LeadStatus.INTERESTED.value, LeadStatus.NOT_INTERESTED.value, LeadStatus.NEUTRAL.value, LeadStatus.NEEDS_FOLLOWUP.value} else LeadStatus.REPLIED.value
                crud.update_lead_status(
                    session,
                    lead_email=matching,
                    status=status,
                    reply_category=category,
                    thread_id=message.get("thread_id"),
                )
                crud.log_email_event(
                    session,
                    lead_email=matching,
                    event_type="INBOUND_REPLY",
                    status="CLASSIFIED",
                    subject=message.get("subject"),
                    gmail_message_id=message.get("message_id"),
                    metadata={"category": category, "snippet": message.get("snippet")},
                )

            updated_leads = crud.list_leads(session)
        return calculate_metrics(updated_leads)
