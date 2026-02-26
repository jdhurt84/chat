from __future__ import annotations

from datetime import datetime

from app.alerts.digest import write_daily_digest
from app.alerts.emailer import send_digest_email
from app.classify.classifier import classify_trigger
from app.config import DEFAULT_INSTITUTIONS, DEFAULT_TRIGGER_TERMS
from app.dedupe.merge import dedupe_signals
from app.ingestion.rss_sources import fetch_google_news_rss
from app.ingestion.sample_sources import fetch_sample_articles
from app.models.types import Article, Signal
from app.scoring.rules import opportunity_score, route_from_score, urgency_from_score
from app.storage.db import get_state, init_db, insert_signal, set_state, source_url_exists

TARGET_ACCOUNTS = {
    "hotchkiss school",
    "jacksonville country day school",
}


def _default_article_provider(use_live: bool) -> list[Article]:
    articles: list[Article] = []
    if use_live:
        for institution in DEFAULT_INSTITUTIONS:
            for trigger in DEFAULT_TRIGGER_TERMS[:3]:
                query = f"{institution} {trigger}"
                try:
                    articles.extend(fetch_google_news_rss(query=query, max_items=5))
                except Exception:
                    continue
    if not articles:
        articles = fetch_sample_articles()
    return articles


def run_daily_update(use_live: bool = True, article_provider=None, email_delivery: bool = True) -> tuple[list[Signal], str, bool]:
    init_db()
    provider = article_provider or (lambda: _default_article_provider(use_live=use_live))
    last_run_iso = get_state("last_run_at")
    last_run = datetime.fromisoformat(last_run_iso) if last_run_iso else None

    raw_articles = provider()
    filtered_articles: list[Article] = []
    for article in raw_articles:
        if source_url_exists(article.source_url):
            continue
        if last_run and article.published_date <= last_run:
            continue
        filtered_articles.append(article)

    new_signals: list[Signal] = []
    for article in filtered_articles:
        trigger, confidence, reason = classify_trigger(article)
        org_key = article.organization_name.strip().lower()
        is_target = org_key in TARGET_ACCOUNTS
        is_profile_similar = article.sector in {"private school", "boarding school", "university", "hospital", "event venue"}

        score = opportunity_score(
            trigger=trigger,
            region=article.region,
            is_target_account=is_target,
            is_profile_similar=is_profile_similar,
            published_date=article.published_date,
            source_type=article.source_type,
        )
        signal = Signal(
            organization_name=article.organization_name,
            region=article.region,
            sector=article.sector,
            trigger_category=trigger,
            confidence_score=confidence,
            opportunity_score=score,
            urgency=urgency_from_score(score),
            reason=reason,
            source_url=article.source_url,
            published_date=article.published_date,
            source_type=article.source_type,
            route=route_from_score(score),
        )
        new_signals.append(signal)

    merged = dedupe_signals(new_signals)
    for signal in merged:
        insert_signal(signal)

    set_state("last_run_at", datetime.utcnow().isoformat())
    digest_path = write_daily_digest(merged)
    emailed = send_digest_email(str(digest_path)) if email_delivery else False
    return merged, str(digest_path), emailed
