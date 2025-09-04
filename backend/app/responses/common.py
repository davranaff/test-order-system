from pydantic import BaseModel, Field


class MessageResponse(BaseModel):

    message: str = Field(..., description="Сообщение")
    success: bool = Field(default=True, description="Статус успеха")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Операция выполнена успешно",
                "success": True
            }
        }


class ErrorResponse(BaseModel):

    error: str = Field(..., description="Сообщение об ошибке")
    details: dict = Field(default=None, description="Детали ошибки")
    success: bool = Field(default=False, description="Статус успеха")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Товар не найден",
                "details": {"product_id": "550e8400-e29b-41d4-a716-446655440000"},
                "success": False
            }
        }
