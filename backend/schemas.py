from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ==================== Activity 스키마 ====================

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    instructor: Optional[str] = None
    max_participants: int = 20
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    activity_date: Optional[datetime] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    instructor: Optional[str] = None
    max_participants: Optional[int] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    activity_date: Optional[datetime] = None


class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime
    booking_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


# ==================== User 스키마 ====================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Subscription 스키마 ====================

class SubscriptionBase(BaseModel):
    plan_type: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SubscriptionCreate(SubscriptionBase):
    user_id: int


class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Booking 스키마 ====================

class BookingBase(BaseModel):
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    user_id: int
    activity_id: int


class BookingResponse(BookingBase):
    id: int
    user_id: int
    activity_id: int
    booking_date: datetime
    
    class Config:
        from_attributes = True


# ==================== Volunteer 스키마 ====================

class VolunteerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    availability: Optional[str] = None
    experience: Optional[str] = None


class VolunteerCreate(VolunteerBase):
    activity_id: int


class VolunteerResponse(VolunteerBase):
    id: int
    activity_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

