from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.product import Product


class ProductResponse(Product):

    id: UUID
    name: str
    price: float
    category: str
    is_available: bool
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):

    products: List[ProductResponse]
    total: int = Field(..., description="Общее количество товаров")
    page: int = Field(..., description="Текущая страница")
    limit: int = Field(..., description="Количество товаров на странице")

    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "_id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Пицца Маргарита",
                        "price": 450.0,
                        "category": "Пицца",
                        "is_available": True,
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-01T12:00:00"
                    }
                ],
                "total": 25,
                "page": 1,
                "limit": 10
            }
        }