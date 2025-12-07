from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class NewsItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source: str
    title: str
    summary: Optional[str] = None
    url: str
    published_at: Optional[datetime] = None
    fetched_at: datetime
