import json
import logging
from uuid import UUID
from fastapi import WebSocket, WebSocketDisconnect, Depends
from fastapi.routing import APIRouter

from app.websocket.connection_manager import ConnectionManager
from app.dependencies import get_connection_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/{role}")
async def websocket_endpoint(
    websocket: WebSocket,
    role: str,
    manager: ConnectionManager = Depends(get_connection_manager)
):

    if role not in ["customers", "staff", "admin"]:
        await websocket.close(code=4000)
        return

    await manager.connect(websocket, role)

    try:
        while True:

            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                await handle_websocket_message(websocket, message, manager)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from {role} client")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"{role.capitalize()} client disconnected")


async def handle_websocket_message(websocket: WebSocket, message: dict, manager: ConnectionManager):

    message_type = message.get("type")

    if message_type == "subscribe_order":

        order_id = message.get("order_id")
        if order_id:
            try:
                order_uuid = UUID(order_id)
                await manager.subscribe_to_order(websocket, order_uuid)
                await websocket.send_text(json.dumps({
                    "type": "subscribed",
                    "order_id": order_id
                }))
            except ValueError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid order ID format"
                }))

    elif message_type == "ping":
        await websocket.send_text(json.dumps({"type": "pong"}))

    else:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Unknown message type"
        }))
