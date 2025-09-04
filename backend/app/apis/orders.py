import logging
from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks

from app.services.order import OrderService
from app.dto.order import OrderCreate, OrderStatusUpdate
from app.responses.order import OrderResponse, OrderListResponse
from app.models.order import OrderStatus
from app.exceptions import OrderNotFoundError, ProductNotFoundError, DatabaseError, ValidationError
from app.dependencies import get_order_service, get_connection_manager
from app.websocket.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    service: OrderService = Depends(get_order_service),
    connection_manager: ConnectionManager = Depends(get_connection_manager)
):

    try:
        new_order = await service.create_order(order)
        logger.info(f"Order created via API: {new_order.id}")

        background_tasks.add_task(
            connection_manager.broadcast_new_order,
            new_order.model_dump(mode='json')
        )

        return new_order

    except ProductNotFoundError as e:
        logger.warning(f"Product not found during order creation: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        logger.warning(f"Validation error during order creation: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in create_order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=OrderListResponse)
async def get_orders(
    status: Optional[OrderStatus] = Query(None, description="Фильтр по статусу"),
    customer_name: Optional[str] = Query(None, description="Поиск по имени клиента"),
    date_from: Optional[datetime] = Query(None, description="Дата начала периода"),
    date_to: Optional[datetime] = Query(None, description="Дата окончания периода"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(10, ge=1, le=100, description="Количество заказов на странице"),
    service: OrderService = Depends(get_order_service)
):

    try:
        orders, total = await service.get_orders(
            status=status,
            customer_name=customer_name,
            date_from=date_from,
            date_to=date_to,
            page=page,
            limit=limit
        )

        return OrderListResponse(
            orders=[o.model_dump() for o in orders],
            total=total,
            page=page,
            limit=limit
        )
    except DatabaseError as e:
        logger.error(f"Database error in get_orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service)
):

    try:
        order = await service.get_order(order_id)
        return order
    except OrderNotFoundError as e:
        logger.warning(f"Order not found in API: {order_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in get_order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    status_update: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    service: OrderService = Depends(get_order_service),
    connection_manager: ConnectionManager = Depends(get_connection_manager)
):

    try:
        updated_order = await service.update_order_status(order_id, status_update.status)
        logger.info(f"Order status updated via API: {order_id} -> {status_update.status}")

        background_tasks.add_task(
            connection_manager.broadcast_order_update,
            order_id,
            updated_order.model_dump(mode='json')
        )

        stats = await service.get_orders_statistics()
        background_tasks.add_task(
            connection_manager.broadcast_statistics_update,
            stats
        )

        return updated_order

    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.warning(f"Invalid status transition: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in update_order_status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}", response_model=OrderResponse)
async def cancel_order(
    order_id: UUID,
    background_tasks: BackgroundTasks,
    service: OrderService = Depends(get_order_service),
    connection_manager: ConnectionManager = Depends(get_connection_manager)
):

    try:
        cancelled_order = await service.cancel_order(order_id)
        logger.info(f"Order cancelled via API: {order_id}")

        background_tasks.add_task(
            connection_manager.broadcast_order_update,
            order_id,
            cancelled_order.model_dump(mode='json')
        )

        return cancelled_order

    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error in cancel_order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/overview")
async def get_statistics(
    service: OrderService = Depends(get_order_service)
):

    try:
        stats = await service.get_orders_statistics()
        logger.info("Statistics requested via API")
        return {"statistics": stats}
    except DatabaseError as e:
        logger.error(f"Database error in get_statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
