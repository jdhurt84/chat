from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from app.scoring.rules import opportunity_score, route_from_score


class ScoringTests(unittest.TestCase):
    def test_high_score_routes_to_instant_alert(self) -> None:
        score = opportunity_score(
            trigger="facility_upgrade",
            region="Northeast",
            is_target_account=True,
            is_profile_similar=True,
            published_date=datetime.utcnow() - timedelta(days=1),
            source_type="press_release",
        )
        self.assertGreaterEqual(score, 75)
        self.assertEqual(route_from_score(score), "instant_alert")

    def test_low_score_routes_to_store_only(self) -> None:
        score = opportunity_score(
            trigger="peer_influence",
            region="Midwest",
            is_target_account=False,
            is_profile_similar=False,
            published_date=datetime.utcnow() - timedelta(days=40),
            source_type="social",
        )
        self.assertLess(score, 50)
        self.assertEqual(route_from_score(score), "store_only")


if __name__ == "__main__":
    unittest.main()
