from __future__ import annotations

import argparse
import time

from app.jobs.daily_update import run_daily_update


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitoring & Trigger Intelligence daily runner")
    parser.add_argument("--sample-only", action="store_true", help="Use bundled sample data only")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    parser.add_argument("--interval-hours", type=int, default=24, help="Polling interval in hours for daemon mode")
    parser.add_argument("--no-email", action="store_true", help="Disable email delivery for this run")
    return parser.parse_args()


def run_once(sample_only: bool, no_email: bool) -> None:
    signals, digest_path, emailed = run_daily_update(use_live=not sample_only, email_delivery=not no_email)
    print(f"Processed {len(signals)} new signals")
    print(f"Digest written to {digest_path}")
    print(f"Email delivered: {emailed}")
    for signal in signals:
        print(f"- {signal.organization_name} | {signal.trigger_category} | {signal.opportunity_score} | {signal.route}")


def main() -> None:
    args = parse_args()
    run_once(sample_only=args.sample_only, no_email=args.no_email)
    if not args.daemon:
        return

    interval_seconds = max(1, args.interval_hours) * 3600
    while True:
        time.sleep(interval_seconds)
        run_once(sample_only=args.sample_only, no_email=args.no_email)


if __name__ == "__main__":
    main()
