from datetime import datetime, date, timezone
import requests
from sqlmodel import select, Session
from app.config import get_settings
from app.models import Ephemerides

settings = get_settings()

def get_or_refresh_ephemerides(session: Session):
    today = date.today()

    stmt = select(Ephemerides).where(Ephemerides.date == today)
    existing = session.exec(stmt).first()
    if existing:
        return existing

    url = f"https://api.sunrise-sunset.org/json?lat={settings.latitude}&lng={settings.longitude}&formatted=0"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()["results"]

    sunrise = datetime.fromisoformat(data["sunrise"])
    sunset = datetime.fromisoformat(data["sunset"])

    day_length = data["day_length"]

    eph = Ephemerides(
        date=today,
        created_at=datetime.now(timezone.utc),
        sunrise=sunrise.time(),
        sunset=sunset.time(),
        day_length_seconds=int(day_length),
        moon_phase_label="unknown",
        moon_phase_value=None,
    )
    session.add(eph)
    session.commit()
    session.refresh(eph)
    return eph
