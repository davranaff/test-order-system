from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.customer import Customer
from app.models.order import OrderStatus
from app.dto.order_item import OrderItemCreate


class OrderCreate(BaseModel):
    customer: Customer = Field(..., description="Информация о клиенте")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Список позиций заказа")
    notes: Optional[str] = Field(None, description="Дополнительные примечания к заказу")
    delivery_address: Optional[str] = Field(None, description="Адрес доставки")
    delivery_time: Optional[datetime] = Field(None, description="Время доставки")

    class Config:
        json_schema_extra = {
            "example": {
                "customer": {
                    "name": "Иван Петров",
                    "phone": "+998901234567",
                    "email": "ivan.petrov@example.com"
                },
                "items": [
                    {
                        "product_id": "550e8400-e29b-41d4-a716-446655440001",
                        "quantity": 2,
                        "special_requests": "Без лука"
                    }
                ],
                "notes": "Быстрая доставка",
                "delivery_address": "г. Ташкент, ул. Навои 15"
            }
        }


class OrderUpdate(BaseModel):
    customer: Optional[Customer] = Field(None, description="Информация о клиенте")
    status: Optional[OrderStatus] = Field(None, description="Статус заказа")
    notes: Optional[str] = Field(None, description="Дополнительные примечания к заказу")
    delivery_address: Optional[str] = Field(None, description="Адрес доставки")
    delivery_time: Optional[datetime] = Field(None, description="Время доставки")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "подтвержден",
                "notes": "Клиент просил перезвонить за час до доставки",
                "delivery_time": "2024-01-01T18:00:00"
            }
        }


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="Новый статус заказа")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "готов"
            }
        }
