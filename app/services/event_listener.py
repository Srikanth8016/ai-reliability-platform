import asyncio
import json

from app.core.redis import redis_client
from app.core.events import EVENT_CHANNEL
from app.websocket.manager import manager


async def listen_for_events():

    pubsub = redis_client.pubsub()
    pubsub.subscribe(EVENT_CHANNEL)

    print(
        f"Subscribed to {EVENT_CHANNEL}"
    )

    while True:

        message = pubsub.get_message(
            ignore_subscribe_messages=True
        )

        if message:

            event = json.loads(
                message["data"]
            )

            await manager.broadcast(event)

        await asyncio.sleep(0.1)
