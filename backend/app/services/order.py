import logging
from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import Binary

from app.models.order import Order, OrderItem, OrderStatus
from app.dto.order import OrderCreate
from app.exceptions import OrderNotFoundError, ProductNotFoundError, DatabaseError
from app.services.product import ProductService

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, db_client: MongoClient, product_service: ProductService):
        self.db = db_client.restaurant_db
        self.collection = self.db.orders
        self.product_service = product_service

    async def create_order(self, order_data: OrderCreate) -> Order:

        try:

            order_items = []
            total_amount = 0.0

            for item_data in order_data.items:

                product = await self.product_service.get_product(item_data.product_id)

                if not product.is_available:
                    raise ProductNotFoundError(f"Product {product.name} is not available")


                order_item = OrderItem(
                    id=product.id,
                    name=product.name,
                    quantity=item_data.quantity,
                    price=product.price,
                    special_requests=item_data.special_requests
                )

                order_items.append(order_item)
                total_amount += order_item.total_price


            order = Order(
                customer=order_data.customer,
                items=order_items,
                total_amount=total_amount,
                notes=order_data.notes,
                delivery_address=order_data.delivery_address,
                delivery_time=order_data.delivery_time
            )


            result = self.collection.insert_one(order.model_dump(by_alias=True))

            if result.inserted_id:
                logger.info(f"Order created successfully: {order.id}, total: {total_amount}")
                return order
            else:
                raise DatabaseError("Failed to create order")

        except (ProductNotFoundError, DatabaseError):
            raise
        except PyMongoError as e:
            logger.error(f"Database error creating order: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def get_order(self, order_id: UUID) -> Optional[Order]:

        try:
            order_data = self.collection.find_one({"_id": Binary.from_uuid(order_id)})

            if not order_data:
                logger.warning(f"Order not found: {order_id}")
                raise OrderNotFoundError(f"Order {order_id} not found")

            order_data["id"] = order_id
            del order_data["_id"]

            return Order(**order_data)

        except PyMongoError as e:
            logger.error(f"Database error getting order {order_id}: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def get_orders(self,
        status: Optional[OrderStatus] = None,
        customer_name: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        page: int = 1,
        limit: int = 10
    ) -> tuple[List[Order], int]:

        try:
            filter_query = {}

            if status:
                filter_query["status"] = status.value
            if customer_name:
                filter_query["customer.name"] = {"$regex": customer_name, "$options": "i"}
            if date_from or date_to:
                date_filter = {}
                if date_from:
                    date_filter["$gte"] = date_from
                if date_to:
                    date_filter["$lte"] = date_to
                filter_query["created_at"] = date_filter


            total = self.collection.count_documents(filter_query)


            cursor = self.collection.find(filter_query).sort("created_at", -1).skip((page - 1) * limit).limit(limit)

            orders = []
            for order_data in cursor:
                print(order_data, 'ORDERED')
                order_data["id"] = order_data["_id"]
                del order_data["_id"]
                orders.append(Order(**order_data))

            logger.info(f"Retrieved {len(orders)} orders (page {page}, total {total})")
            return orders, total

        except PyMongoError as e:
            logger.error(f"Database error getting orders: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def update_order_status(self, order_id: UUID, new_status: OrderStatus) -> Order:

        try:

            order = await self.get_order(order_id)


            if not self._is_valid_status_transition(order.status, new_status):
                raise ValueError(f"Invalid status transition: {order.status} -> {new_status}")

            print(new_status, order_id, "!@")
            result = self.collection.update_one(
                {"_id": Binary.from_uuid(order_id)},
                {
                    "$set": {
                        "status": new_status.value,
                        "updated_at": datetime.utcnow()
                    }
                }
            )

            if result.modified_count > 0:
                logger.info(f"Order status updated: {order_id} -> {new_status.value}")
                return await self.get_order(order_id)
            else:
                return order

        except (OrderNotFoundError, ValueError):
            raise
        except PyMongoError as e:
            logger.error(f"Database error updating order status {order_id}: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def cancel_order(self, order_id: UUID) -> Order:
        return await self.update_order_status(order_id, OrderStatus.CANCELLED)

    async def get_orders_statistics(self) -> Dict[str, int]:
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1}
                    }
                }
            ]
            result = list(self.collection.aggregate(pipeline))

            stats = {status.value: 0 for status in OrderStatus}

            for item in result:
                if item["_id"] in stats:
                    stats[item["_id"]] = item["count"]

            logger.info(f"Orders statistics retrieved: {stats}")

            return stats
        except PyMongoError as e:
            logger.error(f"Database error getting statistics: {e}")
            raise DatabaseError(f"Database error: {str(e)}")

    def _is_valid_status_transition(self, current: OrderStatus, new: OrderStatus) -> bool:
        valid_transitions = {
            OrderStatus.NEW: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED],
            OrderStatus.READY: [OrderStatus.COMPLETED, OrderStatus.CANCELLED],
            OrderStatus.COMPLETED: [],
            OrderStatus.CANCELLED: [],
        }

        return new in valid_transitions.get(current, [])