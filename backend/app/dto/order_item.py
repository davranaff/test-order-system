from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: UUID = Field(..., description="ID товара")
    quantity: int = Field(..., ge=1, description="Количество")
    special_requests: Optional[str] = Field(None, description="Особые пожелания")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "550e8400-e29b-41d4-a716-446655440001",
                "quantity": 2,
                "special_requests": "Без лука, добавить острый соус"
            }
        }
