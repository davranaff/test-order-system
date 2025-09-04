from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class BaseDocument(BaseModel):

    id: UUID = Field(default_factory=uuid4, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
