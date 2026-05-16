from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import PERSONAS_DIR
from .models import PersonaId
from .store import upsert_persona


@dataclass(frozen=True)
class PersonaSeed:
    id: PersonaId
    title: str
    summary: str
    md_filename: str


PERSONA_SEEDS: tuple[PersonaSeed, ...] = (
    PersonaSeed(
        id="scanner",
        title="Scanner",
        summary="Needs quick summaries, low friction, and obvious next actions.",
        md_filename="scanner.md",
    ),
    PersonaSeed(
        id="comparer",
        title="Comparer",
        summary="Needs visible filters, sorting, evidence, and tradeoffs.",
        md_filename="comparer.md",
    ),
    PersonaSeed(
        id="explorer",
        title="Explorer",
        summary="Needs suggestions, branching paths, and discovery-oriented grouping.",
        md_filename="explorer.md",
    ),
    PersonaSeed(
        id="expert_operator",
        title="Expert Operator",
        summary="Needs dense controls, minimal explanation, and quick operation.",
        md_filename="expert_operator.md",
    ),
)


def persona_path(persona_id: PersonaId) -> Path:
    for seed in PERSONA_SEEDS:
        if seed.id == persona_id:
            return PERSONAS_DIR / seed.md_filename
    raise ValueError(f"Unknown persona: {persona_id}")


def ensure_personas_seeded() -> None:
    for seed in PERSONA_SEEDS:
        path = PERSONAS_DIR / seed.md_filename
        upsert_persona(seed.id, seed.title, str(path), seed.summary)


def read_persona_md(persona_id: PersonaId) -> str:
    path = persona_path(persona_id)
    return path.read_text(encoding="utf-8")


def append_persona_changelog(persona_id: PersonaId, entry: str) -> None:
    path = persona_path(persona_id)
    existing = path.read_text(encoding="utf-8")
    marker = "## Changelog\n"
    if marker not in existing:
        updated = f"{existing.rstrip()}\n\n{marker}\n{entry}\n"
    else:
        updated = existing.replace(marker, f"{marker}\n{entry}\n", 1)
    path.write_text(updated, encoding="utf-8")

