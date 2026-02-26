from __future__ import annotations

from datetime import date
from pathlib import Path

from app.models.types import Signal


def write_daily_digest(signals: list[Signal], output_dir: str = "outputs") -> Path:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    digest_path = Path(output_dir) / f"daily_digest_{date.today().isoformat()}.md"

    lines = [
        f"# Daily Monitoring Digest ({date.today().isoformat()})",
        "",
        f"Total new signals: {len(signals)}",
        "",
    ]

    if not signals:
        lines.append("No new qualifying signals found today.")
    else:
        for signal in sorted(signals, key=lambda s: s.opportunity_score, reverse=True):
            lines.extend(
                [
                    f"## {signal.organization_name} — {signal.trigger_category}",
                    f"- Score: {signal.opportunity_score} ({signal.route})",
                    f"- Confidence: {signal.confidence_score}",
                    f"- Reason: {signal.reason}",
                    f"- Source: {signal.source_url}",
                    "",
                ]
            )

    digest_path.write_text("\n".join(lines), encoding="utf-8")
    return digest_path
