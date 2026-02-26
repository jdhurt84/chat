from __future__ import annotations

import unittest

from app.ingestion.rss_sources import parse_rss


RSS_SAMPLE = """
<rss><channel>
  <item>
    <title>Sample headline</title>
    <link>https://example.org/a</link>
    <description>Strategic plan announced</description>
    <pubDate>Tue, 02 Jan 2024 10:00:00 GMT</pubDate>
  </item>
</channel></rss>
"""


class RssIngestionTests(unittest.TestCase):
    def test_parse_rss(self) -> None:
        items = parse_rss(RSS_SAMPLE)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "Sample headline")
        self.assertEqual(items[0].link, "https://example.org/a")


if __name__ == "__main__":
    unittest.main()
