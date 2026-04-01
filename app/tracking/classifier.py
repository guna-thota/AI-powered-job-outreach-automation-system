"""Reply classification service."""

from __future__ import annotations

from app.constants import REPLY_CATEGORIES
from app.personalization.llm_engine import LLMEngine


class ReplyClassifier:
    """Classifies inbound replies into business actions."""

    def __init__(self) -> None:
        self.llm_engine = LLMEngine()

    def classify(self, reply_text: str) -> str:
        """Classify and normalize output to allowed categories."""
        category = self.llm_engine.classify_reply(reply_text)
        if category not in REPLY_CATEGORIES:
            return "NEEDS_FOLLOWUP"
        return category
