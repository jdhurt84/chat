# How to Run This MVP

## 1) Daily manual run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --no-email
```

This performs one update cycle and writes a digest file under `outputs/`.

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

## 3) Fully local run (no network)

```bash
python main.py --sample-only --no-email
```

## 4) Auto-update every day

```bash
python main.py --daemon --interval-hours 24
```

Keep this process running (tmux/screen/systemd/PM2) to receive daily updates automatically.

## 5) API mode

```bash
uvicorn app.api.main:app --reload
```

- `POST /run` triggers one daily update cycle.
- `GET /signals` returns stored signals.

## 6) How incremental updates work
- New articles are fetched from RSS sources (or sample source).
- Existing `source_url` values are ignored.
- Articles older than `last_run_at` are ignored.
- New signals are scored and included in that day’s digest.
