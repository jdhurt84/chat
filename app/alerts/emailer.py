from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


class EmailConfigError(ValueError):
    pass


def _get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise EmailConfigError(f"Missing required environment variable: {name}")
    return value


def send_digest_email(digest_path: str, dry_run: bool = False) -> bool:
    enabled = os.getenv("EMAIL_ENABLED", "false").strip().lower() == "true"
    if not enabled:
        return False

    digest_file = Path(digest_path)
    if not digest_file.exists():
        raise FileNotFoundError(f"Digest file not found: {digest_path}")

    smtp_host = _get_required_env("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = _get_required_env("SMTP_USER")
    smtp_password = _get_required_env("SMTP_PASSWORD")
    smtp_from = _get_required_env("SMTP_FROM")
    smtp_to = _get_required_env("SMTP_TO")

    subject = os.getenv("SMTP_SUBJECT", "Daily Monitoring Digest")
    body = digest_file.read_text(encoding="utf-8")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp_from
    message["To"] = smtp_to
    message.set_content(body)

    if dry_run:
        return True

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    return True
