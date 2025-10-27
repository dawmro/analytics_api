from datetime import datetime, timezone
from typing import List, Optional
import sqlmodel
from sqlmodel import SQLModel, Field



def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )


class EventCreateModel(SQLModel):
    page: str
    description: Optional[str] = Field(default="default description")


class EventUpdateModel(SQLModel):
    description: str


class EventListModel(SQLModel):
    results: List[EventModel]
    count: int
