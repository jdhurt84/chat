from __future__ import annotations

from app.models.types import Signal


def dedupe_key(signal: Signal) -> str:
    day_bucket = signal.published_date.strftime("%Y-%m-%d")
    return f"{signal.organization_name.lower()}::{signal.trigger_category}::{day_bucket}"


def dedupe_signals(signals: list[Signal]) -> list[Signal]:
    seen: dict[str, Signal] = {}
    for signal in signals:
        key = dedupe_key(signal)
        existing = seen.get(key)
        if existing is None or signal.opportunity_score > existing.opportunity_score:
            seen[key] = signal
    return list(seen.values())
