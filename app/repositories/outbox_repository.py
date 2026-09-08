import json
from datetime import datetime

from sqlalchemy import select

from app.models.outbox_event import OutboxEvent


def create_outbox_event(
    db,
    event_type: str,
    payload: dict,
):
    event = OutboxEvent(
        event_type=event_type,
        payload=json.dumps(payload),
    )

    db.add(event)

    return event


def get_unpublished_events(
    db,
    limit: int = 100,
):
    result = db.execute(
        select(OutboxEvent)
        .where(
            OutboxEvent.published.is_(False)
        )
        .order_by(OutboxEvent.id)
        .limit(limit)
    )

    return result.scalars().all()


def mark_event_published(
    event,
):
    event.published = True
    event.published_at = datetime.utcnow()
