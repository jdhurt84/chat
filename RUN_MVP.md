# How to Run This MVP

## How to trigger it (direct answer)

### Trigger immediately from terminal

```bash
python main.py --no-email
```

### Trigger immediately with sample data

```bash
python main.py --sample-only --no-email
```

### Trigger through API

```bash
uvicorn app.api.main:app --reload
curl -X POST "http://127.0.0.1:8000/run?sample_only=false&no_email=false"
```

### Trigger every day automatically

```bash
python main.py --daemon --interval-hours 24
```

or with cron:

```cron
0 7 * * * cd /workspace/chat && /usr/bin/python3 main.py >> /workspace/chat/run.log 2>&1
```

---

## 1) Initial setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Enable email delivery

```bash
export EMAIL_ENABLED=true
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER="you@example.com"
export SMTP_PASSWORD="app-password"
export SMTP_FROM="you@example.com"
export SMTP_TO="team@example.com"
python main.py
```

## 3) How incremental updates work
- New articles are fetched from RSS sources (or sample source).
- Existing `source_url` values are ignored.
- Articles older than `last_run_at` are ignored.
- New signals are scored and included in that day’s digest.
