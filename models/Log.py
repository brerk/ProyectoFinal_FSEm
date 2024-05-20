from dataclasses import dataclass
from datetime import datetime


@dataclass
class Log:
    action: str
    status: str
    timestamp: datetime
    id: int = 0
