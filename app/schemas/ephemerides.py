from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict


class EphemeridesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    created_at: datetime
    sunrise: time
    sunset: time
    day_length_seconds: int
    moon_phase_label: str | None
    moon_phase_value: float | None
