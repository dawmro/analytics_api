import os
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from api.db.session import get_session
from .models import (
    EventCreateModel,
    EventUpdateModel,
    EventModel,
    EventListModel
)
from api.db.config import DATABASE_URL

router = APIRouter()


@router.get("/", response_model=EventListModel)
def read_events(session: Session = Depends(get_session)):
    query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    results = session.exec(query).all()
    return {
        "results": results,
        "count": len(results)
    }


@router.post("/", response_model=EventModel)
def create_event(
        payload:EventCreateModel, 
        session: Session = Depends(get_session)):
    data = payload.model_dump() # payload -> dict -> pydantic
    obj = EventModel.model_validate(data)
    session.add(obj) # prepare to add
    session.commit() # add to db
    session.refresh(obj) # get info about object

    return obj


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