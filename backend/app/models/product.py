from typing import Optional
from pydantic import Field

from app.models.base import BaseDocument


class Product(BaseDocument):

    name: str = Field(..., description="Название товара")
    price: float = Field(..., ge=0, description="Цена товара")
    category: str = Field(..., description="Категория товара")
    is_available: bool = Field(default=True, description="Доступность к заказу")
    description: Optional[str] = Field(None, description="Описание товара")

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Пицца Маргарита",
                "price": 450.0,
                "category": "Пицца",
                "is_available": True,
                "description": "Классическая пицца с томатным соусом, моцареллой и базиликом",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }
