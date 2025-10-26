import os
from fastapi import APIRouter
from .models import (
    EventCreateModel,
    EventUpdateModel,
    EventModel,
    EventListModel
)
from api.db.config import DATABASE_URL

router = APIRouter()


@router.get("/")
def read_events() -> EventListModel:
    print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    return {
        "results": [
            {"id": 1}, 
            {"id": 2}, 
            {"id": 3}
        ],
        "count": 3
    }


@router.post("/")
def create_event(payload:EventCreateModel) -> EventModel:
    print(payload.page, type(payload.page))
    data = payload.model_dump() # payload -> dict -> pydantic
    return {
        "id": 123,
        **data
    }


@router.get("/{event_id}")
def get_event(event_id:int) -> EventModel:
    return {
        "id": event_id
    }


@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateModel) -> EventModel:
    print(payload.description, type(payload.description))
    data = payload.model_dump() # payload -> dict -> pydantic
    return {
        "id": event_id,
        **data
    }