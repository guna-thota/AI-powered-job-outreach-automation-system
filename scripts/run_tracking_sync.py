"""Execute inbox sync and reply classification pipeline."""

from app.tracking.tracker import TrackingPipeline
from app.utils.logger import configure_logging

if __name__ == "__main__":
    configure_logging()
    metrics = TrackingPipeline().sync_replies()
    print(metrics)
