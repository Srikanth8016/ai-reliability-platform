from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("/events")
async def websocket_events(websocket: WebSocket):

    await manager.connect(websocket)

    try:

        while True:
            data = await websocket.receive_text()

            print(
                f"WebSocket message: {data}"
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
