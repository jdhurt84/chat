from __future__ import annotations

from app.models.types import Signal


def render_alert(signal: Signal) -> str:
    return (
        f"Alert: {signal.organization_name} — {signal.trigger_category}\n"
        f"Score: {signal.opportunity_score}\n"
        f"Why flagged: {signal.reason}\n"
        f"Source: {signal.source_url}"
    )
