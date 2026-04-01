"""SQLAlchemy engine/session setup."""

from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.database.models import Base

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """Create all tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session() -> Session:
    """Yield a database session with transaction safety."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
