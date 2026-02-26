from __future__ import annotations

from datetime import datetime, timedelta

from app.models.types import Article


def fetch_sample_articles() -> list[Article]:
    now = datetime.utcnow()
    return [
        Article(
            organization_name="Hotchkiss School",
            region="Northeast",
            sector="private school",
            title="Hotchkiss reopens reimagined dining commons",
            body="The campus announced a major dining commons renovation with expanded seating and modern systems.",
            source_url="https://example.org/hotchkiss-dining",
            published_date=now - timedelta(days=2),
            source_type="local_news",
        ),
        Article(
            organization_name="Jacksonville Country Day School",
            region="Florida",
            sector="private school",
            title="School publishes strategic plan for student life",
            body="The strategic plan and community vision include investment in campus experience.",
            source_url="https://example.org/jcds-strategic-plan",
            published_date=now - timedelta(days=5),
            source_type="strategic_plan",
        ),
        Article(
            organization_name="Quinnipiac University",
            region="Northeast",
            sector="university",
            title="Dining hall renovation adds allergen-free kitchen",
            body="Trustees approved renovation and all-you-care-to-eat model transformation.",
            source_url="https://example.org/quinnipiac-dining",
            published_date=now - timedelta(days=1),
            source_type="press_release",
        ),
    ]
