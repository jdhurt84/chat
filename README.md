# Monitoring & Trigger Intelligence MVP (Starter)

Runnable starter implementation for daily ingestion, classification, scoring, dedupe, persistence, digest generation, and optional email delivery.

## Quick start (daily update run)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --no-email
```

What happens each run:
- Pulls live Google News RSS results for configured institutions (falls back to sample data if network/source fails).
- Skips previously seen article URLs and older-than-last-run items.
- Scores and routes new signals.
- Writes a markdown digest to `outputs/daily_digest_YYYY-MM-DD.md`.
- Optionally emails the digest when email is enabled.

## Email delivery setup
Set these environment variables:

```bash
export EMAIL_ENABLED=true
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER="you@example.com"
export SMTP_PASSWORD="app-password"
export SMTP_FROM="you@example.com"
export SMTP_TO="team@example.com"
export SMTP_SUBJECT="Daily Monitoring Digest"
```

Then run:

```bash
python main.py
```

## Run in sample-only mode

```bash
python main.py --sample-only --no-email
```

## Run continuously every 24h

```bash
python main.py --daemon --interval-hours 24
```

## Run API

```bash
uvicorn app.api.main:app --reload
```

Endpoints:
- `GET /health`
- `POST /run?sample_only=true|false&no_email=true|false`
- `GET /signals`

## Run tests

```bash
python -m unittest discover -s tests -v
```
