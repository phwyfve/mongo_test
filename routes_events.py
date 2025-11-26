from fastapi import APIRouter, HTTPException
from events import Event

router = APIRouter()

@router.post("/events")
async def create_event(event: Event):
    await event.insert()
    return event

@router.get("/events/{event_id}")
async def get_event(event_id: str):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}")
async def update_event(event_id: str, data: dict):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in data.items():
        setattr(event, key, value)
    await event.save()
    return event

@router.delete("/events/{event_id}")
async def delete_event(event_id: str):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await event.delete()
    return {"status": "deleted"}
