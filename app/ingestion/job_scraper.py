"""Optional extension point for job board scraping integrations."""

from __future__ import annotations

from app.utils.logger import get_logger

logger = get_logger(__name__)


def scrape_job_postings() -> list[dict]:
    """Placeholder for future scraping integrations.

    Returns:
        Empty list by default. Replace with production scraping adapter.
    """
    logger.info("Job scraper invoked; no provider configured")
    return []
