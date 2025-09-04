import logging
from pymongo import MongoClient
from fastapi import Depends

from app.services.product import ProductService
from app.services.order import OrderService
from app.websocket.connection_manager import ConnectionManager
from app.settings import get_settings

logger = logging.getLogger(__name__)

_db_client = None
_connection_manager = None


def get_db_client() -> MongoClient:

    global _db_client
    if _db_client is None:
        settings = get_settings()
        _db_client = MongoClient(
            settings.mongodb_url,
            UuidRepresentation="standard",
        )
        logger.info("MongoDB client initialized")
    return _db_client


def get_connection_manager() -> ConnectionManager:

    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
        logger.info("WebSocket connection manager initialized")
    return _connection_manager


def get_product_service(db_client: MongoClient = Depends(get_db_client)) -> ProductService:

    return ProductService(db_client)


def get_order_service(
    db_client: MongoClient = Depends(get_db_client),
    product_service: ProductService = Depends(get_product_service)
) -> OrderService:

    return OrderService(db_client, product_service)
