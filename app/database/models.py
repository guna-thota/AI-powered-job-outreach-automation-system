"""Database and domain models for outreach automation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.constants import LeadStatus


class Base(DeclarativeBase):
    """Base ORM class."""


class LeadORM(Base):
    """Persistent lead entity."""

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    tier: Mapped[str] = mapped_column(String(64), nullable=False, default="B")
    status: Mapped[str] = mapped_column(String(64), nullable=False, default=LeadStatus.NOT_SENT.value)
    last_email_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reply_category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    thread_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class EmailEventORM(Base):
    """Persistent audit trail for sent emails and tracking events."""

    __tablename__ = "email_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lead_email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gmail_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


@dataclass
class Lead:
    """Domain object used by ingestion and orchestration layers."""

    name: str
    email: str
    company: str
    role: str
    tier: str = "B"
    status: str = LeadStatus.NOT_SENT.value
    id: int | None = None
    last_email_sent_at: datetime | None = None
    reply_category: str | None = None
    thread_id: str | None = None

    @classmethod
    def from_orm(cls, orm_obj: LeadORM) -> "Lead":
        """Map ORM object to domain model."""
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            email=orm_obj.email,
            company=orm_obj.company,
            role=orm_obj.role,
            tier=orm_obj.tier,
            status=orm_obj.status,
            last_email_sent_at=orm_obj.last_email_sent_at,
            reply_category=orm_obj.reply_category,
            thread_id=orm_obj.thread_id,
        )
