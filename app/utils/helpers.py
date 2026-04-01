"""General-purpose utility helpers."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def project_root() -> Path:
    """Resolve repository root using this file location."""
    return Path(__file__).resolve().parents[2]


def load_jinja_template(template_path: str):
    """Load Jinja2 template by project-relative path."""
    path = project_root() / template_path
    env = Environment(
        loader=FileSystemLoader(path.parent),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )
    return env.get_template(path.name)
