from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    age = Column(Integer)
    address = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subscriptions = relationship("Subscription", back_populates="user")
    bookings = relationship("ActivityBooking", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # 도예/공예, 수영, 커피 시음 등
    location = Column(String(200), nullable=False)
    instructor = Column(String(100))
    max_participants = Column(Integer, default=20)
    duration_minutes = Column(Integer)  # 활동 시간 (분)
    price = Column(Float)  # 정가 (구독으로 할인)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    activity_date = Column(DateTime)  # 활동 일시
    
    bookings = relationship("ActivityBooking", back_populates="activity")
    volunteers = relationship("Volunteer", back_populates="activity")
    
    # 계산 필드 (API 응답용)
    booking_count = 0


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(String(50), nullable=False)  # monthly, annual 등
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")


class ActivityBooking(Base):
    __tablename__ = "activity_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)  # 특별 요청사항
    
    user = relationship("User", back_populates="bookings")
    activity = relationship("Activity", back_populates="bookings")


class Volunteer(Base):
    __tablename__ = "volunteers"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    availability = Column(String(200))  # 가능한 시간
    experience = Column(Text)  # 관련 경험
    created_at = Column(DateTime, default=datetime.utcnow)
    
    activity = relationship("Activity", back_populates="volunteers")

