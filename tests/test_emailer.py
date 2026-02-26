from __future__ import annotations

import os
import tempfile
import unittest

from app.alerts.emailer import EmailConfigError, send_digest_email


class EmailerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._backup = dict(os.environ)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._backup)

    def test_disabled_email_returns_false(self) -> None:
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("digest")
            path = f.name
        self.assertFalse(send_digest_email(path, dry_run=True))

    def test_enabled_email_requires_config(self) -> None:
        os.environ["EMAIL_ENABLED"] = "true"
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("digest")
            path = f.name
        with self.assertRaises(EmailConfigError):
            send_digest_email(path, dry_run=True)

    def test_dry_run_success(self) -> None:
        os.environ["EMAIL_ENABLED"] = "true"
        os.environ["SMTP_HOST"] = "smtp.example.com"
        os.environ["SMTP_PORT"] = "587"
        os.environ["SMTP_USER"] = "user"
        os.environ["SMTP_PASSWORD"] = "pass"
        os.environ["SMTP_FROM"] = "from@example.com"
        os.environ["SMTP_TO"] = "to@example.com"

        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("digest")
            path = f.name

        self.assertTrue(send_digest_email(path, dry_run=True))


if __name__ == "__main__":
    unittest.main()
