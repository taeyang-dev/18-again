from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uvicorn

from database import SessionLocal, engine, Base
from models import Activity, User, Subscription, ActivityBooking, Volunteer
from schemas import (
    ActivityCreate, ActivityResponse, ActivityUpdate,
    UserCreate, UserResponse,
    SubscriptionCreate, SubscriptionResponse,
    BookingCreate, BookingResponse,
    VolunteerCreate, VolunteerResponse
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="시니어 체험 플랫폼",
    description="시니어들을 위한 구독형 체험 예약 플랫폼",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== 활동(Activity) 관련 엔드포인트 ====================

@app.get("/api/activities", response_model=List[ActivityResponse])
def get_activities(
    category: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """모든 체험 활동 조회 (카테고리, 지역별 필터링 가능)"""
    query = db.query(Activity)
    
    if category:
        query = query.filter(Activity.category == category)
    if location:
        query = query.filter(Activity.location.contains(location))
    
    activities = query.all()
    return activities


@app.get("/api/activities/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """특정 체험 활동 상세 조회"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다")
    
    # 신청자 수 계산
    booking_count = db.query(ActivityBooking).filter(
        ActivityBooking.activity_id == activity_id
    ).count()
    activity.booking_count = booking_count
    
    return activity


@app.post("/api/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """새로운 체험 활동 생성"""
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@app.put("/api/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db)
):
    """체험 활동 정보 수정"""
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다")
    
    update_data = activity_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_activity, key, value)
    
    db.commit()
    db.refresh(db_activity)
    return db_activity


# ==================== 사용자 관련 엔드포인트 ====================

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """새로운 사용자 등록"""
    # 이메일 중복 확인
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """사용자 정보 조회"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


# ==================== 구독 관련 엔드포인트 ====================

@app.post("/api/subscriptions", response_model=SubscriptionResponse)
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    """구독 생성"""
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == subscription.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    db_subscription = Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


@app.get("/api/users/{user_id}/subscription", response_model=Optional[SubscriptionResponse])
def get_user_subscription(user_id: int, db: Session = Depends(get_db)):
    """사용자의 활성 구독 조회"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()
    return subscription


# ==================== 체험 예약 관련 엔드포인트 ====================

@app.post("/api/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """체험 활동 예약"""
    # 활동 존재 확인
    activity = db.query(Activity).filter(Activity.id == booking.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다")
    
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == booking.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 구독 확인
    subscription = db.query(Subscription).filter(
        Subscription.user_id == booking.user_id,
        Subscription.is_active == True
    ).first()
    if not subscription:
        raise HTTPException(
            status_code=400,
            detail="활성 구독이 필요합니다"
        )
    
    # 중복 예약 확인
    existing_booking = db.query(ActivityBooking).filter(
        ActivityBooking.activity_id == booking.activity_id,
        ActivityBooking.user_id == booking.user_id
    ).first()
    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="이미 예약된 활동입니다"
        )
    
    db_booking = ActivityBooking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@app.get("/api/activities/{activity_id}/bookings", response_model=List[BookingResponse])
def get_activity_bookings(activity_id: int, db: Session = Depends(get_db)):
    """특정 활동의 예약 목록 조회"""
    bookings = db.query(ActivityBooking).filter(
        ActivityBooking.activity_id == activity_id
    ).all()
    return bookings


@app.get("/api/users/{user_id}/bookings", response_model=List[BookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    """사용자의 예약 목록 조회"""
    bookings = db.query(ActivityBooking).filter(
        ActivityBooking.user_id == user_id
    ).all()
    return bookings


@app.delete("/api/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """예약 취소"""
    booking = db.query(ActivityBooking).filter(
        ActivityBooking.id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다")
    
    db.delete(booking)
    db.commit()
    return {"message": "예약이 취소되었습니다"}


# ==================== 자원봉사자 관련 엔드포인트 ====================

@app.post("/api/volunteers", response_model=VolunteerResponse)
def create_volunteer(volunteer: VolunteerCreate, db: Session = Depends(get_db)):
    """자원봉사자 신청"""
    # 활동 존재 확인
    activity = db.query(Activity).filter(Activity.id == volunteer.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다")
    
    db_volunteer = Volunteer(**volunteer.dict())
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer


@app.get("/api/activities/{activity_id}/volunteers", response_model=List[VolunteerResponse])
def get_activity_volunteers(activity_id: int, db: Session = Depends(get_db)):
    """특정 활동의 자원봉사자 목록 조회"""
    volunteers = db.query(Volunteer).filter(
        Volunteer.activity_id == activity_id
    ).all()
    return volunteers


@app.get("/api/categories")
def get_categories():
    """활동 카테고리 목록 반환"""
    return {
        "categories": [
            "도예/공예",
            "수영",
            "커피 시음",
            "요가/필라테스",
            "요리 클래스",
            "원예",
            "음악/악기",
            "독서 모임",
            "기타"
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

