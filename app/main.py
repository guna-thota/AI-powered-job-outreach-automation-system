"""Application entrypoint for outreach send pipeline."""

from __future__ import annotations

from app.database import crud
from app.database.db import get_session, init_db
from app.email.email_service import EmailService
from app.ingestion.csv_loader import load_leads
from app.utils.logger import configure_logging, get_logger

logger = get_logger(__name__)


def run_outreach(csv_path: str = "data/leads.csv") -> None:
    """Load leads, upsert them in DB, and send outreach emails."""
    init_db()
    leads = load_leads(csv_path)
    with get_session() as session:
        crud.upsert_leads(session, leads)
        targets = crud.get_pending_outreach_leads(session)

    service = EmailService()
    for lead in targets:
        service.send_cold_email(lead)

    logger.info("Outreach complete. Processed %s lead(s)", len(targets))


def main() -> None:
    configure_logging()
    run_outreach()


if __name__ == "__main__":
    main()
