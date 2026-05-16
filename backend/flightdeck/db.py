from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3

from .config import MIGRATIONS_DIR, database_path


def connect() -> sqlite3.Connection:
    db_path = database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def session():
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def run_migrations() -> None:
    with session() as conn:
      conn.execute(
          """
          CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
          )
          """
      )
      applied = {
          row["version"]
          for row in conn.execute("SELECT version FROM schema_migrations").fetchall()
      }

      for path in sorted(Path(MIGRATIONS_DIR).glob("*.sql")):
          version = path.stem
          if version in applied:
              continue
          conn.executescript(path.read_text(encoding="utf-8"))
          conn.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))

