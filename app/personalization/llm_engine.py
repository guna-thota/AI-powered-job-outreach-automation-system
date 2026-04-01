"""OpenAI-backed LLM adapter for personalization and classification."""

from __future__ import annotations

from openai import OpenAI

from app.config import settings
from app.personalization.prompt_templates import CLASSIFICATION_PROMPT, PERSONALIZATION_PROMPT


class LLMEngine:
    """Wrapper around OpenAI SDK with reusable methods."""

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate_personalized_line(self, *, name: str, company: str, role: str, tier: str) -> str:
        """Generate personalized opening line for cold outreach."""
        prompt = PERSONALIZATION_PROMPT.format(name=name, company=company, role=role, tier=tier)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.4,
            max_output_tokens=120,
        )
        return (response.output_text or "").strip()

    def classify_reply(self, email_text: str) -> str:
        """Classify a reply into campaign action categories."""
        prompt = CLASSIFICATION_PROMPT.format(email_text=email_text)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0,
            max_output_tokens=10,
        )
        return (response.output_text or "NEEDS_FOLLOWUP").strip().upper()
