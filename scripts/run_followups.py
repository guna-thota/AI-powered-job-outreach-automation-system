"""Execute follow-up scheduler job."""

from app.scheduler.followup_scheduler import run_followup_job
from app.utils.logger import configure_logging

if __name__ == "__main__":
    configure_logging()
    run_followup_job()
