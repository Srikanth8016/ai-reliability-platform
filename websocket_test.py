import asyncio

import websockets


async def main():

    uri = "ws://127.0.0.1:8000/api/v1/ws/events?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzg4OTI3MzgxfQ.GXghtlytc4PCq0srdTW8akeEgoEJgLF-ZvoOa1Zm_Fk"

    async with websockets.connect(uri) as websocket:

        print("Connected!")

        await websocket.send("Hello Server")

        while True:
            message = await websocket.recv()

            print(
                f"Received: {message}"
            )


asyncio.run(main())
