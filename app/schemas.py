from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ResourceCreate(BaseModel):
    name: str
    type: str


class ResourceOut(ResourceCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime


class BookingOut(BookingCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
