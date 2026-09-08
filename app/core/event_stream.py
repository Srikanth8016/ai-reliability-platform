import json

from app.core.redis import redis_client

STREAM_NAME = "reliability:events:stream"
CONSUMER_GROUP = "reliability-workers"


def add_event(
    event_type: str,
    payload: dict,
):
    event = {
        "type": event_type,
        "payload": json.dumps(payload),
    }

    event_id = redis_client.xadd(
        STREAM_NAME,
        event,
    )

    return event_id


def ensure_consumer_group():
    """Create the consumer group if it doesn't already exist."""
    try:
        redis_client.xgroup_create(
            STREAM_NAME,
            CONSUMER_GROUP,
            id="0",
            mkstream=True,
        )
        print(f"Consumer group '{CONSUMER_GROUP}' created.")
    except Exception:
        # Group already exists — that's fine
        pass
