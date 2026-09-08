import json

from app.core.database import SessionLocal
from app.core.event_stream import add_event
from app.repositories.outbox_repository import (
    get_unpublished_events,
    mark_event_published,
)


def process_outbox():

    db = SessionLocal()

    try:

        events = get_unpublished_events(
            db,
            limit=100,
        )

        if not events:
            print("No unpublished outbox events.")
            return

        print(f"Publishing {len(events)} outbox event(s)...")

        for event in events:

            payload = json.loads(event.payload)

            add_event(
                event.event_type,
                payload,
            )

            mark_event_published(
                event,
            )

            print(
                f"Published: [{event.event_type}] id={event.id}"
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    process_outbox()
