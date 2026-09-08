import json

from app.core.event_stream import (
    CONSUMER_GROUP,
    STREAM_NAME,
    ensure_consumer_group,
)
from app.core.redis import redis_client


def process_event(data: dict):
    event_type = data.get("type")
    payload = json.loads(data.get("payload", "{}"))

    print(f"Stream event: {event_type} → {payload}")

    # Future: route to specific handlers per event_type


def main():
    ensure_consumer_group()

    print(f"Event consumer started. Listening to '{STREAM_NAME}'...")

    consumer_name = "event-consumer-1"

    while True:
        messages = redis_client.xreadgroup(
            groupname=CONSUMER_GROUP,
            consumername=consumer_name,
            streams={STREAM_NAME: ">"},
            count=10,
            block=5000,
        )

        if not messages:
            continue

        for stream, entries in messages:
            for event_id, data in entries:
                try:
                    process_event(data)

                    redis_client.xack(
                        STREAM_NAME,
                        CONSUMER_GROUP,
                        event_id,
                    )

                    print(f"ACK: {event_id}")

                except Exception as exc:
                    print(f"Event {event_id} failed: {exc}")


if __name__ == "__main__":
    main()
