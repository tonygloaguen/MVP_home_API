from datetime import datetime, date, time
from typing import Optional
from sqlmodel import SQLModel, Field

class Ephemerides(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    created_at: datetime
    sunrise: time
    sunset: time
    day_length_seconds: int
    moon_phase_label: Optional[str] = None
    moon_phase_value: Optional[float] = None
