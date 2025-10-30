import os
from typing import List
from datetime import datetime, timedelta, timezone 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import case, func
from timescaledb.hyperfunctions import time_bucket

from api.db.session import get_session
from .models import (
    EventCreateModel,
    EventModel,
    EventBucketModel
)
from api.db.config import DATABASE_URL

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
        "/", "/about", "/pricing", "/contact", 
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]


@router.get("/", response_model=List[EventBucketModel])
def read_events(
        duration: str = Query(default='1 day'),
        pages: List = Query(default=None),
        session: Session = Depends(get_session)
    ):
    os_case = case(
        (EventModel.user_agent.ilike('%windows%'), 'Windows'),
        (EventModel.user_agent.ilike('%macintosh%'), 'MacOS'),
        (EventModel.user_agent.ilike('%iphone%'), 'iOS'),
        (EventModel.user_agent.ilike('%android%'), 'Android'),
        (EventModel.user_agent.ilike('%linux%'), 'Linux'),
        else_='Other'
    ).label('operating_system')
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label('bucket'),
            os_case,
            EventModel.page.label('page'),
            func.avg(EventModel.duration).label('avg_duration'),
            func.count().label('count')    
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            os_case,
            EventModel.page
        )
        .order_by(
            bucket,
            os_case,
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


