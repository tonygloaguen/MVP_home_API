from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class RegionalNews(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    source: str
    title: str
    summary: Optional[str] = None
    url: str

    published_at: Optional[datetime] = None
    fetched_at: datetime
