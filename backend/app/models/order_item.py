from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class OrderItem(BaseModel):

    id: UUID = Field(..., description="ID товара")
    name: str = Field(..., description="Название товара на момент заказа")
    quantity: int = Field(..., ge=1, description="Количество")
    price: float = Field(..., ge=0, description="Цена за единицу на момент заказа")
    total_price: float = Field(..., ge=0, description="Общая стоимость позиции")
    special_requests: Optional[str] = Field(None, description="Особые пожелания")

    def __init__(self, **data):
        if 'total' not in data:
            data['total_price'] = data.get('quantity', 0) * data.get('price', 0)
        super().__init__(**data)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Пицца Маргарита",
                "quantity": 2,
                "price": 450.0,
                "total_price": 900.0,
                "special_requests": "Без лука, добавить острый соус"
            }
        }
