from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.customer import Customer
from app.models.order_item import OrderItem
from app.models.enums import OrderStatus
from app.models.order import Order


class OrderResponse(Order):

    id: UUID
    customer: Customer
    items: List[OrderItem]
    status: OrderStatus
    total_amount: float
    notes: Optional[str]
    delivery_address: Optional[str]
    delivery_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):

    orders: List[OrderResponse]
    total: int = Field(..., description="Общее количество заказов")
    page: int = Field(..., description="Текущая страница")
    limit: int = Field(..., description="Количество заказов на странице")

    class Config:
        json_schema_extra = {
            "example": {
                "orders": [
                    {
                        "_id": "550e8400-e29b-41d4-a716-446655440002",
                        "customer": {
                            "name": "Иван Петров",
                            "phone": "+998901234567",
                            "email": "ivan.petrov@example.com"
                        },
                        "items": [
                            {
                                "product_id": "550e8400-e29b-41d4-a716-446655440001",
                                "product_name": "Пицца Маргарита",
                                "quantity": 2,
                                "unit_price": 450.0,
                                "total_price": 900.0
                            }
                        ],
                        "status": "новый",
                        "total_amount": 900.0,
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-01T12:00:00"
                    }
                ],
                "total": 50,
                "page": 1,
                "limit": 10
            }
        }
