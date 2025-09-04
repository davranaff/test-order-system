import json
import logging
from typing import Dict, Set
from uuid import UUID
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:

    def __init__(self):

        self.active_connections: Dict[str, Set[WebSocket]] = {
            "customers": set(),
            "staff": set(),
            "admin": set()
        }


        self.order_subscribers: Dict[UUID, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, role: str = "customers"):

        await websocket.accept()
        self.active_connections[role].add(websocket)
        logger.info(f"New {role} connection established. Total: {len(self.active_connections[role])}")

    def disconnect(self, websocket: WebSocket):

        for role, connections in self.active_connections.items():
            if websocket in connections:
                connections.remove(websocket)
                logger.info(f"{role.capitalize()} disconnected. Remaining: {len(connections)}")
                break


        for order_id, subscribers in self.order_subscribers.items():
            subscribers.discard(websocket)

    async def subscribe_to_order(self, websocket: WebSocket, order_id: UUID):

        if order_id not in self.order_subscribers:
            self.order_subscribers[order_id] = set()

        self.order_subscribers[order_id].add(websocket)
        logger.info(f"Client subscribed to order {order_id}")

    async def broadcast_to_role(self, message: dict, role: str):

        if role not in self.active_connections:
            return

        message_str = json.dumps(message, default=str)
        disconnected = set()

        for connection in self.active_connections[role]:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Error sending message to {role}: {e}")
                disconnected.add(connection)


        for connection in disconnected:
            self.active_connections[role].discard(connection)

    async def broadcast_order_update(self, order_id: UUID, order_data: dict):

        message = {
            "type": "order_update",
            "order_id": str(order_id),
            "data": order_data
        }


        await self.broadcast_to_role(message, "staff")
        await self.broadcast_to_role(message, "admin")


        if order_id in self.order_subscribers:
            message_str = json.dumps(message, default=str)
            disconnected = set()

            for connection in self.order_subscribers[order_id]:
                try:
                    await connection.send_text(message_str)
                except Exception as e:
                    logger.error(f"Error sending order update to subscriber: {e}")
                    disconnected.add(connection)


            for connection in disconnected:
                self.order_subscribers[order_id].discard(connection)

    async def broadcast_new_order(self, order_data: dict):

        message = {
            "type": "new_order",
            "data": order_data
        }


        await self.broadcast_to_role(message, "staff")
        await self.broadcast_to_role(message, "admin")

    async def broadcast_statistics_update(self, stats: dict):

        message = {
            "type": "statistics_update",
            "data": stats
        }


        await self.broadcast_to_role(message, "admin")

    def get_connections_count(self) -> dict:

        return {
            role: len(connections)
            for role, connections in self.active_connections.items()
        }
