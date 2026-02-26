from __future__ import annotations

import os
import unittest
from datetime import datetime, timedelta

from app.jobs.daily_update import run_daily_update
from app.models.types import Article
from app.storage.db import DB_PATH, init_db


class DailyUpdateTests(unittest.TestCase):
    def setUp(self) -> None:
        if DB_PATH.exists():
            os.remove(DB_PATH)
        init_db()

    def test_incremental_behavior(self) -> None:
        now = datetime.utcnow()
        article = Article(
            organization_name="Test Academy",
            region="Northeast",
            sector="private school",
            title="Campus dining renovation approved",
            body="The board approved facility upgrades.",
            source_url="https://example.org/test-1",
            published_date=now - timedelta(hours=1),
            source_type="local_news",
        )

        provider = lambda: [article]
        first_signals, _, _ = run_daily_update(use_live=False, article_provider=provider, email_delivery=False)
        second_signals, _, _ = run_daily_update(use_live=False, article_provider=provider, email_delivery=False)

        self.assertEqual(len(first_signals), 1)
        self.assertEqual(len(second_signals), 0)


if __name__ == "__main__":
    unittest.main()
