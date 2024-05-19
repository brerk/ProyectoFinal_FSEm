from pydantic import BaseModel
from datetime import datetime


class RiegoConfig(BaseModel):
    time: str  # HH:MM
    duration: int  # Time on
    min_temp: int
    max_temp: int

    timestamp: datetime
