import os
from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/{event_id}", response_model=EventModel)
def get_event(
        event_id:int, 
        session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.put("/{event_id}", response_model=EventModel)
def update_event(
        event_id:int, 
        payload:EventUpdateModel, 
        session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    
    data = payload.model_dump() # payload -> dict -> pydantic
    for k,v in data.items(): # iterate over key and vaule of each item
        setattr(obj, k ,v) # assign value for key in object
    session.add(obj) # prepare to add
    session.commit() # add to db
    session.refresh(obj) # get info about object

    return obj