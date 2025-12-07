from datetime import datetime, timedelta
from typing import List
import xml.etree.ElementTree as ET

import requests
from sqlmodel import Session, select

from app.config import get_settings
from app.models import RegionalNews

settings = get_settings()


def _now_utc() -> datetime:
    return datetime.utcnow()


def _parse_rss(xml_text: str, source_label: str) -> list[RegionalNews]:
    root = ET.fromstring(xml_text)

    # RSS classique : <rss><channel><item>...</item></channel></rss>
    channel = root.find("channel")
    if channel is None:
        # Certains flux utilisent des namespaces -> fallback
        # On parcourt tous les items
        items = root.findall(".//item")
    else:
        items = channel.findall("item")

    news_list: list[RegionalNews] = []
    now = _now_utc()

    for item in items[:10]:  # on limite à 10 items pour le dashboard
        title_el = item.find("title")
        desc_el = item.find("description")
        link_el = item.find("link")
        pub_el = item.find("pubDate")

        title = title_el.text.strip() if title_el is not None and title_el.text else "Sans titre"
        summary = desc_el.text.strip() if desc_el is not None and desc_el.text else None
        url = link_el.text.strip() if link_el is not None and link_el.text else "#"

        # Published_at : on reste simple → on stocke brut en texte parsé au mieux
        published_at = None
        if pub_el is not None and pub_el.text:
            try:
                # Beaucoup de RSS : "Mon, 02 Dec 2024 12:34:56 GMT"
                published_at = datetime.strptime(pub_el.text.strip(), "%a, %d %b %Y %H:%M:%S %Z")
            except Exception:
                # On ignore les erreurs de parsing
                published_at = None

        news_list.append(
            RegionalNews(
                source=source_label,
                title=title,
                summary=summary,
                url=url,
                published_at=published_at,
                fetched_at=now,
            )
        )

    return news_list


def _fetch_news_from_rss() -> list[RegionalNews]:
    url = settings.news_rss_url
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    xml_text = resp.text

    return _parse_rss(xml_text, source_label=url)
    

def get_or_refresh_news(session: Session, limit: int = 5) -> list[RegionalNews]:
    """
    Retourne une liste d'actualités régionales.
    Rafraîchit à partir du RSS si TTL dépassé.
    """
    # On regarde la dernière date de fetch
    stmt_last = select(RegionalNews).order_by(RegionalNews.fetched_at.desc()).limit(1)
    last = session.exec(stmt_last).first()

    now = _now_utc()
    ttl = timedelta(minutes=settings.news_ttl_minutes)

    if last is None or now - last.fetched_at > ttl:
        try:
            # On vide l'ancienne table (optionnel, mais propre pour un MVP)
            session.exec("DELETE FROM regionalnews")
        except Exception:
            # Selon le dialecte SQLite, on peut juste ignorer si ça coince
            pass

        try:
            fresh_items = _fetch_news_from_rss()
            for item in fresh_items:
                session.add(item)
            session.commit()
        except Exception as e:
            print(f"[news_service] Erreur lors du fetch RSS : {e}")

    # On récupère les N plus récents
    stmt = (
        select(RegionalNews)
        .order_by(RegionalNews.published_at.desc().nullslast(), RegionalNews.fetched_at.desc())
        .limit(limit)
    )
    return list(session.exec(stmt))
