from __future__ import annotations

from datetime import datetime, timedelta

from app.models.types import TriggerCategory, SourceType

TRIGGER_WEIGHTS: dict[TriggerCategory, int] = {
    "leadership_change": 20,
    "strategic_plan_campaign": 18,
    "facility_upgrade": 25,
    "enrollment_boarding_shift": 15,
    "program_innovation": 12,
    "feedback": 15,
    "financial_pressure": 20,
    "non_core_campus_use": 10,
    "vendor_rotation": 10,
    "peer_influence": 8,
}

SOURCE_WEIGHTS: dict[SourceType, int] = {
    "press_release": 15,
    "board_material": 15,
    "strategic_plan": 15,
    "local_news": 10,
    "social": 3,
    "other": 5,
}


def geographic_fit(region: str) -> int:
    normalized = region.strip().lower()
    if normalized in {"northeast", "florida"}:
        return 15
    if normalized in {"mid-atlantic", "southeast", "new england"}:
        return 8
    return 0


def account_fit(is_target_account: bool, is_profile_similar: bool) -> int:
    if is_target_account:
        return 20
    if is_profile_similar:
        return 10
    return 0


def freshness(published_date: datetime, now: datetime | None = None) -> int:
    current = now or datetime.utcnow()
    age = current - published_date
    if age <= timedelta(days=7):
        return 15
    if age <= timedelta(days=30):
        return 8
    return 0


def evidence_quality(source_type: SourceType) -> int:
    return SOURCE_WEIGHTS[source_type]


def opportunity_score(
    trigger: TriggerCategory,
    region: str,
    is_target_account: bool,
    is_profile_similar: bool,
    published_date: datetime,
    source_type: SourceType,
) -> int:
    return (
        TRIGGER_WEIGHTS[trigger]
        + geographic_fit(region)
        + account_fit(is_target_account, is_profile_similar)
        + freshness(published_date)
        + evidence_quality(source_type)
    )


def route_from_score(score: int) -> str:
    if score >= 75:
        return "instant_alert"
    if score >= 50:
        return "daily_digest"
    return "store_only"


def urgency_from_score(score: int) -> str:
    if score >= 75:
        return "high"
    if score >= 50:
        return "medium"
    return "low"
