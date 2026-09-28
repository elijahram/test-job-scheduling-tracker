from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


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
