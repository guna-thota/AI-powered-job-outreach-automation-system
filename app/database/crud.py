"""CRUD helpers for lead and event persistence."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import LeadStatus
from app.database.models import EmailEventORM, Lead, LeadORM


def upsert_leads(session: Session, leads: Iterable[Lead]) -> list[Lead]:
    """Insert or update leads by email address."""
    persisted: list[Lead] = []
    for lead in leads:
        existing = session.scalar(select(LeadORM).where(LeadORM.email == lead.email))
        if existing:
            existing.name = lead.name
            existing.company = lead.company
            existing.role = lead.role
            existing.tier = lead.tier
            row = existing
        else:
            row = LeadORM(
                name=lead.name,
                email=lead.email,
                company=lead.company,
                role=lead.role,
                tier=lead.tier,
                status=lead.status,
            )
            session.add(row)
            session.flush()
        persisted.append(Lead.from_orm(row))
    return persisted


def list_leads(session: Session) -> list[Lead]:
    """Return all leads ordered by most recently updated."""
    rows = session.scalars(select(LeadORM).order_by(LeadORM.updated_at.desc())).all()
    return [Lead.from_orm(row) for row in rows]


def get_pending_outreach_leads(session: Session) -> list[Lead]:
    """Leads eligible for first outreach email."""
    rows = session.scalars(
        select(LeadORM).where(LeadORM.status.in_([LeadStatus.NOT_SENT.value, LeadStatus.FAILED.value]))
    ).all()
    return [Lead.from_orm(row) for row in rows]


def update_lead_status(
    session: Session,
    lead_email: str,
    status: str,
    reply_category: str | None = None,
    thread_id: str | None = None,
) -> None:
    """Update lead status and metadata."""
    lead = session.scalar(select(LeadORM).where(LeadORM.email == lead_email))
    if not lead:
        return
    lead.status = status
    if status in {LeadStatus.SENT.value, LeadStatus.FOLLOWUP_SENT.value}:
        lead.last_email_sent_at = datetime.utcnow()
    if reply_category:
        lead.reply_category = reply_category
    if thread_id:
        lead.thread_id = thread_id


def log_email_event(
    session: Session,
    lead_email: str,
    event_type: str,
    status: str,
    subject: str | None = None,
    gmail_message_id: str | None = None,
    metadata: dict | None = None,
) -> None:
    """Create auditable email event entry."""
    row = EmailEventORM(
        lead_email=lead_email,
        event_type=event_type,
        subject=subject,
        gmail_message_id=gmail_message_id,
        status=status,
        metadata_json=json.dumps(metadata or {}),
    )
    session.add(row)


def list_email_events(session: Session) -> list[EmailEventORM]:
    """Return event log rows."""
    return session.scalars(select(EmailEventORM).order_by(EmailEventORM.created_at.desc())).all()
