from typing import Optional
from pydantic import BaseModel, Field


class Customer(BaseModel):

    name: str = Field(..., min_length=1, description="Имя клиента")
    phone: Optional[str] = Field(None, description="Телефон клиента")
    email: Optional[str] = Field(None, description="Email клиента")
    address: Optional[str] = Field(None, description="Адрес клиента")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Иван Петров",
                "phone": "+998901234567",
                "email": "ivan.petrov@example.com",
                "address": "г. Ташкент, ул. Навои 15"
            }
        }
