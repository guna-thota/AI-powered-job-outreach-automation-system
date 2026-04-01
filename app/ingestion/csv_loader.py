"""CSV ingestion module for lead records."""

from __future__ import annotations

import csv
from pathlib import Path

from app.database.models import Lead

REQUIRED_FIELDS = {"name", "email", "company", "role", "tier"}


def load_leads(file_path: str | Path) -> list[Lead]:
    """Load leads from CSV with schema validation."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Lead CSV not found: {path}")

    leads: list[Lead] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED_FIELDS.issubset(reader.fieldnames):
            raise ValueError(f"CSV must include columns: {sorted(REQUIRED_FIELDS)}")
        for index, row in enumerate(reader, start=2):
            if not row.get("email"):
                raise ValueError(f"Missing email at line {index}")
            leads.append(
                Lead(
                    name=row["name"].strip(),
                    email=row["email"].strip().lower(),
                    company=row["company"].strip(),
                    role=row["role"].strip(),
                    tier=(row.get("tier") or "B").strip().upper(),
                    status=(row.get("status") or "NOT_SENT").strip().upper(),
                )
            )
    return leads
