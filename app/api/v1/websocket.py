from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.security import decode_access_token
from app.websocket.manager import manager

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("/events")
async def websocket_events(
    websocket: WebSocket,
):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    user_id = decode_access_token(token)

    if not user_id:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)

    try:

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
