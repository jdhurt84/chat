from __future__ import annotations

import sqlite3
from pathlib import Path

from app.models.types import Signal

DB_PATH = Path("monitoring.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_name TEXT NOT NULL,
                region TEXT NOT NULL,
                sector TEXT NOT NULL,
                trigger_category TEXT NOT NULL,
                confidence_score INTEGER NOT NULL,
                opportunity_score INTEGER NOT NULL,
                urgency TEXT NOT NULL,
                reason TEXT NOT NULL,
                source_url TEXT NOT NULL,
                published_date TEXT NOT NULL,
                source_type TEXT NOT NULL,
                route TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_signals_source_url ON signals(source_url)")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )


def insert_signal(signal: Signal) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO signals (
                organization_name, region, sector, trigger_category,
                confidence_score, opportunity_score, urgency, reason,
                source_url, published_date, source_type, route, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                signal.organization_name,
                signal.region,
                signal.sector,
                signal.trigger_category,
                signal.confidence_score,
                signal.opportunity_score,
                signal.urgency,
                signal.reason,
                signal.source_url,
                signal.published_date.isoformat(),
                signal.source_type,
                signal.route,
                signal.created_at.isoformat(),
            ),
        )


def list_signals(limit: int = 100) -> list[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM signals ORDER BY published_date DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()


def source_url_exists(source_url: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM signals WHERE source_url = ? LIMIT 1",
            (source_url,),
        ).fetchone()
        return row is not None


def get_state(key: str) -> str | None:
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM app_state WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None


def set_state(key: str, value: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO app_state(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
