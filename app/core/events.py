import json

from app.core.redis import redis_client

EVENT_CHANNEL = "reliability:events"


def publish_event(
    event_type: str,
    payload: dict,
):

    event = {
        "type": event_type,
        "payload": payload,
    }

    redis_client.publish(
        EVENT_CHANNEL,
        json.dumps(event),
    )
