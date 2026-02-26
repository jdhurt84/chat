from __future__ import annotations

from app.jobs.daily_update import run_daily_update
from app.models.types import Signal


def run_poll() -> list[Signal]:
    signals, _, _ = run_daily_update(use_live=False, email_delivery=False)
    return signals


if __name__ == "__main__":
    results = run_poll()
    for signal in results:
        print(f"{signal.organization_name}: {signal.opportunity_score} ({signal.route})")
