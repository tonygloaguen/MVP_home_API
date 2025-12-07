from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.services import get_or_refresh_ephemerides
from app.schemas import EphemeridesRead

router = APIRouter(prefix="/api/ephemerides", tags=["ephemerides"])

@router.get("/", response_model=EphemeridesRead)
def ephemerides(session: Session = Depends(get_session)):
    return get_or_refresh_ephemerides(session)
