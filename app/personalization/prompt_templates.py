"""Prompt templates for LLM personalization and classification."""

PERSONALIZATION_PROMPT = """
You are writing a concise, professional cold-email opening line.

Lead details:
- Name: {name}
- Company: {company}
- Role: {role}
- Tier: {tier}

Write 1-2 sentences max. Be specific and natural.
""".strip()

CLASSIFICATION_PROMPT = """
Classify the following email reply into exactly one category:
INTERESTED, NOT_INTERESTED, NEUTRAL, NEEDS_FOLLOWUP.

Reply text:
{email_text}

Return only the category word.
""".strip()
