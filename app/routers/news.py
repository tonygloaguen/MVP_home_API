from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.services import get_or_refresh_news
from app.schemas import NewsItemRead

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/", response_model=list[NewsItemRead])
def news(session: Session = Depends(get_session)):
    items = get_or_refresh_news(session, limit=5)
    # Pydantic v2 : model_validate pour chaque élément
    return [NewsItemRead.model_validate(n) for n in items]
