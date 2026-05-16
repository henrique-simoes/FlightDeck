from __future__ import annotations

from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
MIGRATIONS_DIR = BACKEND_DIR / "migrations"
PERSONAS_DIR = BACKEND_DIR / "personas"
FRONTEND_DESIGN_PATH = REPO_ROOT / "frontend" / "design.md"


def database_path() -> Path:
    configured = os.getenv("FLIGHTDECK_DB_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return DATA_DIR / "flightdeck.db"


def backend_base_url() -> str:
    return os.getenv("FLIGHTDECK_API_BASE_URL", "http://localhost:8000")

