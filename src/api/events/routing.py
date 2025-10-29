import os
from typing import List
from datetime import datetime, timedelta, timezone 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from timescaledb.hyperfunctions import time_bucket

from api.db.session import get_session
from .models import (
    EventCreateModel,
    EventUpdateModel,
    EventModel,
    EventBucketModel,
    get_utc_now
)
from api.db.config import DATABASE_URL

router = APIRouter()

DEFAULT_LOOKUP_PAGES = ['/about', '/contact', '/pages', '/pricing']


@router.get("/", response_model=List[EventBucketModel])
def read_events(
        duration: str = Query(deafult='1 day'),
        pages: List = Query(default=None),
        session: Session = Depends(get_session)
    ):
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label('bucket'),
            EventModel.page.label('page'),
            func.count().label('count')    
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            EventModel.page
        )
        .order_by(
            bucket,
            EventModel.page
        )
    )
    results = session.exec(query).fetchall()
    return results


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
    obj.updated_at = get_utc_now()
    session.add(obj) # prepare to add
    session.commit() # add to db
    session.refresh(obj) # get info about object

    return obj