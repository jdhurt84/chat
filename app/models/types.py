from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


SourceType = Literal[
    "press_release",
    "board_material",
    "strategic_plan",
    "local_news",
    "social",
    "other",
]

TriggerCategory = Literal[
    "leadership_change",
    "strategic_plan_campaign",
    "facility_upgrade",
    "enrollment_boarding_shift",
    "feedback",
    "program_innovation",
    "financial_pressure",
    "non_core_campus_use",
    "vendor_rotation",
    "peer_influence",
]

Urgency = Literal["low", "medium", "high"]


@dataclass
class Article:
    organization_name: str
    region: str
    sector: str
    title: str
    body: str
    source_url: str
    published_date: datetime
    source_type: SourceType


@dataclass
class Signal:
    organization_name: str
    region: str
    sector: str
    trigger_category: TriggerCategory
    confidence_score: int
    opportunity_score: int
    urgency: Urgency
    reason: str
    source_url: str
    published_date: datetime
    source_type: SourceType
    route: Literal["instant_alert", "daily_digest", "store_only"]
    created_at: datetime = field(default_factory=datetime.utcnow)
