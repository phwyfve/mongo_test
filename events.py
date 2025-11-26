from typing import Optional
from beanie import Document
from pydantic import BaseModel
from datetime import datetime

class Event(Document):
    """Event model for scheduling"""
    start_date: datetime
    event_type: str
    description: Optional[str] = None

    class Settings:
        name = "events"
