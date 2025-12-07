from datetime import datetime, timedelta
import requests
from sqlmodel import select, Session

from app.config import get_settings
from app.models import WeatherSnapshot

settings = get_settings()


def _now_utc() -> datetime:
    """Datetime UTC naïf (sans tzinfo) pour rester compatible SQLite."""
    return datetime.utcnow()


def _fetch_weather_from_api() -> WeatherSnapshot:
    """Appel à l’API OpenWeatherMap (current weather)."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": settings.latitude,
        "lon": settings.longitude,
        "appid": settings.weather_api_key,
        "units": "metric",
        "lang": "fr",
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    now = _now_utc()

    return WeatherSnapshot(
        timestamp=now,
        location=settings.location_name,
        temperature=data["main"]["temp"],
        feels_like=data["main"].get("feels_like"),
        humidity=data["main"].get("humidity"),
        pressure=data["main"].get("pressure"),
        wind_speed=data.get("wind", {}).get("speed"),
        description=(data["weather"][0]["description"] if data.get("weather") else None),
    )


def get_or_refresh_weather(session: Session) -> WeatherSnapshot | None:
    """
    Retourne la météo la plus récente.
    Si l'appel API échoue, on log et on renvoie éventuellement la dernière valeur connue.
    """
    stmt = select(WeatherSnapshot).order_by(WeatherSnapshot.timestamp.desc()).limit(1)
    last = session.exec(stmt).first()

    now = _now_utc()
    ttl = timedelta(minutes=settings.weather_ttl_minutes)

    # On essaie de rafraîchir si pas de données ou TTL dépassé
    if last is None or now - last.timestamp > ttl:
        try:
            snapshot = _fetch_weather_from_api()
            session.add(snapshot)
            session.commit()
            session.refresh(snapshot)
            return snapshot
        except Exception as e:
            # En cas de problème API, on log et on retombe sur la dernière valeur, si elle existe
            print(f"[weather_service] Erreur API météo : {e}")
            return last

    return last
