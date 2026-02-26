from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from app.models.types import Article


@dataclass
class RssItem:
    title: str
    link: str
    description: str
    published_date: datetime


def _safe_text(node: ET.Element | None, default: str = "") -> str:
    if node is None or node.text is None:
        return default
    return node.text.strip()


def parse_rss(xml_text: str) -> list[RssItem]:
    root = ET.fromstring(xml_text)
    items: list[RssItem] = []
    for item in root.findall(".//item"):
        title = _safe_text(item.find("title"), "Untitled")
        link = _safe_text(item.find("link"), "")
        description = _safe_text(item.find("description"), "")
        pub_date_raw = _safe_text(item.find("pubDate"), "")
        try:
            parsed = parsedate_to_datetime(pub_date_raw)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            published_date = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        except Exception:
            published_date = datetime.utcnow()

        items.append(
            RssItem(
                title=title,
                link=link,
                description=description,
                published_date=published_date,
            )
        )
    return items


def _infer_region(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ("connecticut", "new england", "northeast", "massachusetts")):
        return "Northeast"
    if "florida" in lowered or "jacksonville" in lowered:
        return "Florida"
    return "Unknown"


def _infer_sector(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ("academy", "school", "campus")):
        return "private school"
    if any(token in lowered for token in ("hospital", "medical")):
        return "hospital"
    if any(token in lowered for token in ("club", "country club", "golf")):
        return "golf/country club"
    return "education"


def fetch_google_news_rss(query: str, max_items: int = 10) -> list[Article]:
    encoded_query = quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    with urlopen(url, timeout=20) as response:
        xml_text = response.read().decode("utf-8", errors="ignore")

    items = parse_rss(xml_text)
    articles: list[Article] = []
    for item in items[:max_items]:
        text = f"{item.title} {item.description}"
        organization_name = query.split(" strategic plan")[0].split(" dining")[0].strip()
        articles.append(
            Article(
                organization_name=organization_name,
                region=_infer_region(text),
                sector=_infer_sector(text),
                title=item.title,
                body=item.description,
                source_url=item.link,
                published_date=item.published_date,
                source_type="local_news",
            )
        )
    return articles
