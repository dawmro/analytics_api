from typing import List, Optional
from sqlmodel import SQLModel, Field



class EventSchema(SQLModel):
    id: int
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="default description")


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventSchema]
    count: int
