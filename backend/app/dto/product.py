from typing import Optional
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., description="Название товара")
    price: float = Field(..., ge=0, description="Цена товара")
    category: str = Field(..., description="Категория товара")
    is_available: bool = Field(default=True, description="Доступность к заказу")
    description: Optional[str] = Field(None, description="Описание товара")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Пицца Маргарита",
                "price": 450.0,
                "category": "Пицца",
                "is_available": True,
                "description": "Классическая пицца с томатным соусом, моцареллой и базиликом"
            }
        }


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название товара")
    price: Optional[float] = Field(None, ge=0, description="Цена товара")
    category: Optional[str] = Field(None, description="Категория товара")
    is_available: Optional[bool] = Field(None, description="Доступность к заказу")
    description: Optional[str] = Field(None, description="Описание товара")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Пицца Маргарита Большая",
                "price": 550.0,
                "is_available": False
            }
        }
