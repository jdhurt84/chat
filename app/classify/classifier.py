from __future__ import annotations

from app.models.types import Article, TriggerCategory

KEYWORD_TRIGGER_MAP: list[tuple[tuple[str, ...], TriggerCategory, str]] = [
    (("head of school", "ceo", "appointed", "leadership"), "leadership_change", "Leadership change detected in article text."),
    (("strategic plan", "capital campaign", "master plan"), "strategic_plan_campaign", "Strategic planning or campaign language detected."),
    (("dining", "commons", "renovation", "facility", "upgrade"), "facility_upgrade", "Facility or dining upgrade signal found."),
    (("enrollment", "boarding", "expansion"), "enrollment_boarding_shift", "Enrollment/boarding shift mentioned."),
    (("complaint", "dissatisfaction", "parent concern", "student feedback"), "feedback", "Feedback or dissatisfaction pattern identified."),
    (("allergen", "farm-to-school", "wellness", "innovation"), "program_innovation", "Program innovation or wellness signal identified."),
    (("deficit", "budget shortfall", "financial pressure"), "financial_pressure", "Financial pressure indicators identified."),
    (("rentals", "camps", "external events"), "non_core_campus_use", "Non-core campus usage language found."),
    (("vendor change", "contract bid", "provider switch"), "vendor_rotation", "Vendor rotation cue found."),
    (("nearby school", "peer school", "regional competitor"), "peer_influence", "Peer-influence signal found."),
]


def classify_trigger(article: Article) -> tuple[TriggerCategory, int, str]:
    text = f"{article.title} {article.body}".lower()
    for keywords, trigger, reason in KEYWORD_TRIGGER_MAP:
        if any(keyword in text for keyword in keywords):
            return trigger, 82, reason
    return "program_innovation", 55, "No explicit trigger match; defaulted to lowest-risk innovation category."
