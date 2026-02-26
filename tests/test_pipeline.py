from __future__ import annotations

import os
import unittest

from app.jobs.poll_sources import run_poll
from app.storage.db import DB_PATH, init_db, list_signals


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        if DB_PATH.exists():
            os.remove(DB_PATH)
        init_db()

    def test_run_poll_persists_signals(self) -> None:
        signals = run_poll()
        self.assertGreaterEqual(len(signals), 1)
        rows = list_signals(limit=20)
        self.assertEqual(len(rows), len(signals))


if __name__ == "__main__":
    unittest.main()
