from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.services import get_or_refresh_weather
from app.schemas import WeatherRead

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/", response_model=WeatherRead)
def weather(session: Session = Depends(get_session)):
    snapshot = get_or_refresh_weather(session)

    if snapshot is None:
        raise HTTPException(status_code=503, detail="Données météo indisponibles")

    # Pydantic v2 : on utilise model_validate + from_attributes
    return WeatherRead.model_validate(snapshot)
