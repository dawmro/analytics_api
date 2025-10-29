from datetime import datetime, timezone
from typing import List, Optional
import sqlmodel
from sqlmodel import SQLModel, Field
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now



# def get_utc_now():
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

# metric: page visits at given time

class EventModel(TimescaleModel, table=True):
    # id: Optional[int] = Field(default=None, primary_key=True)
    page: str = Field(index=True) # /about /pricing ...
    description: Optional[str] = ""
    # created_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventCreateModel(SQLModel):
    page: str
    description: Optional[str] = Field(default="default description")


class EventUpdateModel(SQLModel):
    description: str


class EventListModel(SQLModel):
    results: List[EventModel]
    count: int


class EventBucketModel(SQLModel):
    bucket: datetime
    page: str
    count: int
