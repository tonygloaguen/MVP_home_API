from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Any, Dict

from app.db import get_session
from app.services import (
    get_or_refresh_weather,
    get_or_refresh_ephemerides,
    get_or_refresh_news,
)
from app.schemas import WeatherRead, EphemeridesRead, NewsItemRead

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/")
def dashboard(session: Session = Depends(get_session)) -> Dict[str, Any]:
    weather = get_or_refresh_weather(session)
    eph = get_or_refresh_ephemerides(session)
    news_items = get_or_refresh_news(session, limit=5)

    if weather is None:
        raise HTTPException(status_code=503, detail="Données météo indisponibles")

    weather_out = WeatherRead.model_validate(weather)
    eph_out = EphemeridesRead.model_validate(eph)
    news_out = [NewsItemRead.model_validate(n) for n in news_items]

    return {
        "weather": weather_out,
        "ephemerides": eph_out,
        "news": news_out,
    }
