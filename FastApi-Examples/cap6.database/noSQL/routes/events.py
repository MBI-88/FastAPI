from fastapi import APIRouter, HTTPException, status
from models.events import Event, EventUpdate
from database.connection import Database
from beanie import PydanticObjectId
from typing import List

# Database config
event_database = Database(Event)

# Routes

event_router = APIRouter(tags=["Events"])


@event_router.get('/', response_model=List[Event])
async def restrive_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get('/{id}', response_model=Event)
async def retrive_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event with supplied ID does not exist")
    return event


@event_router.post('/new')
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {"message": "Event created successfully"}


@event_router.delete('/{id}')
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event with supplied ID does not exist")
    return {"message": "Event deleted successfully"}


@event_router.put('/edit/{id}', response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    event = await event_database.update(id, body)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event with supplied ID does not exists")
    return event
