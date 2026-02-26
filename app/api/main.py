from __future__ import annotations

from app.jobs.daily_update import run_daily_update
from app.storage.db import init_db, list_signals

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover
    FastAPI = None


if FastAPI is not None:
    app = FastAPI(title="Monitoring Trigger Intelligence MVP")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/run")
    def run_once(sample_only: bool = False, no_email: bool = False) -> dict[str, object]:
        signals, digest_path, emailed = run_daily_update(use_live=not sample_only, email_delivery=not no_email)
        return {"processed": len(signals), "digest_path": digest_path, "emailed": emailed}

    @app.get("/signals")
    def get_signals(limit: int = 50) -> list[dict]:
        init_db()
        rows = list_signals(limit=limit)
        return [dict(row) for row in rows]

else:
    app = None
