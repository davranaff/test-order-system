from datetime import datetime
from typing import Optional, List
from pydantic import Field

from app.models.base import BaseDocument
from app.models.customer import Customer
from app.models.order_item import OrderItem
from app.models.enums import OrderStatus


class Order(BaseDocument):

    customer: Customer = Field(..., description="Информация о клиенте")
    items: List[OrderItem] = Field(..., min_items=1, description="Список позиций заказа")
    status: OrderStatus = Field(default=OrderStatus.NEW, description="Статус заказа")
    total_amount: float = Field(..., ge=0, description="Общая сумма заказа")
    notes: Optional[str] = Field(None, description="Дополнительные примечания к заказу")
    delivery_address: Optional[str] = Field(None, description="Адрес доставки")
    delivery_time: Optional[datetime] = Field(None, description="Время доставки")

    def __init__(self, **data):
        if 'total_amount' not in data and 'items' in data:
            data['total_amount'] = sum(item.total_price for item in data['items'])
        super().__init__(**data)

    def update_total_amount(self):
        self.total_amount = sum(item.total_price for item in self.items)

    def update_status(self, new_status: OrderStatus):
        self.status = new_status
        self.updated_at = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "550e8400-e29b-41d4-a716-446655440002",
                "customer": {
                    "name": "Иван Петров",
                    "phone": "+998901234567",
                    "email": "ivan.petrov@example.com"
                },
                "items": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "name": "Пицца Маргарита",
                        "quantity": 2,
                        "unit_price": 450.0,
                        "total_price": 900.0,
                        "special_requests": "Без лука"
                    }
                ],
                "status": "новый",
                "total_amount": 900.0,
                "notes": "Быстрая доставка",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }