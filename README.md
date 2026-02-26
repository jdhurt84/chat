# Monitoring & Trigger Intelligence MVP (Starter)

Runnable starter implementation for daily ingestion, classification, scoring, dedupe, persistence, digest generation, and optional email delivery.

## How to trigger a run

### 1) Trigger once from CLI (most common)

```bash
python main.py --no-email
```

If you want local/sample data only:

```bash
python main.py --sample-only --no-email
```

### 2) Trigger once via API
Start API server:

```bash
uvicorn app.api.main:app --reload
```

Trigger a run:

```bash
curl -X POST "http://127.0.0.1:8000/run?sample_only=false&no_email=false"
```

### 3) Trigger automatically every day

```bash
python main.py --daemon --interval-hours 24
```

### 4) Trigger from cron (recommended for production)
Run `crontab -e` and add:

```cron
0 7 * * * cd /workspace/chat && /usr/bin/python3 main.py >> /workspace/chat/run.log 2>&1
```

## Quick setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

Then trigger:

```bash
python main.py
```

## API endpoints
- `GET /health`
- `POST /run?sample_only=true|false&no_email=true|false`
- `GET /signals`

## Run tests

```bash
python -m unittest discover -s tests -v
```
