# 시니어 체험 플랫폼

시니어들을 위한 구독형 체험 예약 플랫폼입니다. 도예, 수영, 커피 시음 등 다양한 활동을 지역 내에서 찾아 예약하고, 자원봉사자로도 참여할 수 있습니다.

## 주요 기능

- 🎨 **다양한 체험 활동**: 도예/공예, 수영, 커피 시음 등 카테고리별 체험 제공
- 📍 **지역 기반 검색**: 지역별로 활동 필터링 및 검색
- 👥 **신청자 수 확인**: 각 활동에 몇 명이 신청했는지 실시간 확인
- 🤝 **자원봉사자 신청**: 활동에 동행할 자원봉사자 신청 기능
- 📱 **구독형 모델**: 월간/연간 구독으로 여러 활동 참여 가능
- 📋 **예약 관리**: 내 예약 목록 확인 및 취소

## 기술 스택

### 백엔드
- FastAPI (Python)
- SQLAlchemy (ORM)
- SQLite (데이터베이스)

### 프론트엔드
- React 18
- React Router
- Axios
- Vite

## 프로젝트 구조

```
password-checker/
├── backend/
│   ├── main.py              # FastAPI 메인 애플리케이션
│   ├── models.py            # 데이터베이스 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── database.py          # 데이터베이스 설정
│   └── requirements.txt     # Python 의존성
├── frontend/
│   ├── src/
│   │   ├── components/      # React 컴포넌트
│   │   ├── pages/           # 페이지 컴포넌트
│   │   ├── api/             # API 클라이언트
│   │   └── App.jsx          # 메인 앱 컴포넌트
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 설치 및 실행

### 사전 요구사항

- Python 3.8 이상
- Node.js 16 이상
- npm 또는 yarn

### 백엔드 설정

1. 백엔드 디렉토리로 이동:
```bash
cd backend
```

2. Python 가상환경 생성 및 활성화 (권장):
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

4. 서버 실행:
```bash
python main.py
```

또는:
```bash
uvicorn main:app --reload
```

백엔드는 `http://localhost:8000`에서 실행됩니다.
API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

### 프론트엔드 설정

1. 새 터미널에서 프론트엔드 디렉토리로 이동:
```bash
cd frontend
```

2. 의존성 설치:
```bash
npm install
```

3. 개발 서버 실행:
```bash
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

## API 엔드포인트

### 활동 (Activities)
- `GET /api/activities` - 모든 활동 조회 (카테고리, 지역 필터링 가능)
- `GET /api/activities/{id}` - 특정 활동 상세 조회
- `POST /api/activities` - 새 활동 생성
- `GET /api/categories` - 카테고리 목록

### 예약 (Bookings)
- `POST /api/bookings` - 활동 예약
- `GET /api/users/{user_id}/bookings` - 사용자 예약 목록
- `GET /api/activities/{activity_id}/bookings` - 활동별 예약 목록
- `DELETE /api/bookings/{booking_id}` - 예약 취소

### 자원봉사자 (Volunteers)
- `POST /api/volunteers` - 자원봉사자 신청
- `GET /api/activities/{activity_id}/volunteers` - 활동별 자원봉사자 목록

### 사용자 (Users)
- `POST /api/users` - 사용자 등록
- `GET /api/users/{id}` - 사용자 정보 조회

### 구독 (Subscriptions)
- `POST /api/subscriptions` - 구독 생성
- `GET /api/users/{user_id}/subscription` - 사용자 활성 구독 조회

## 사용 예시

### 1. 사용자 등록
```bash
POST /api/users
{
  "name": "홍길동",
  "email": "hong@example.com",
  "phone": "010-1234-5678",
  "age": 65,
  "address": "서울시 강남구"
}
```

### 2. 구독 생성
```bash
POST /api/subscriptions
{
  "user_id": 1,
  "plan_type": "monthly"
}
```

### 3. 활동 예약
```bash
POST /api/bookings
{
  "user_id": 1,
  "activity_id": 1,
  "notes": "휠체어 사용 중입니다"
}
```

### 4. 자원봉사자 신청
```bash
POST /api/volunteers
{
  "activity_id": 1,
  "name": "김봉사",
  "email": "volunteer@example.com",
  "phone": "010-9876-5432",
  "availability": "주중 오전",
  "experience": "노인 돌봄 경험 5년"
}
```

## 데이터베이스

SQLite 데이터베이스가 자동으로 생성됩니다 (`backend/senior_activities.db`).

### 샘플 데이터 초기화

초기 샘플 데이터(사용자, 활동, 구독)를 추가하려면:

```bash
cd backend
python init_data.py
```

이 스크립트는 다음을 생성합니다:
- 샘플 사용자 2명
- 구독 1개
- 샘플 활동 5개 (도예, 수영, 커피 시음, 요가, 요리)

또는 FastAPI의 `/docs` 페이지를 사용하여 직접 데이터를 추가할 수도 있습니다.

## 개발 가이드

### 백엔드 수정 시
- `models.py`: 데이터베이스 모델 수정
- `schemas.py`: API 요청/응답 스키마 수정
- `main.py`: API 엔드포인트 추가/수정

### 프론트엔드 수정 시
- `src/pages/`: 새 페이지 추가
- `src/components/`: 재사용 가능한 컴포넌트 추가
- `src/api/client.js`: API 클라이언트 수정

## 향후 개선 사항

- [ ] 사용자 인증 및 로그인 시스템
- [ ] 결제 시스템 통합
- [ ] 실시간 알림 기능
- [ ] 활동 리뷰 및 평가
- [ ] 관리자 대시보드
- [ ] 모바일 앱 개발
- [ ] 이미지 업로드 기능
- [ ] 지도 통합 (위치 표시)

## 라이선스

이 프로젝트는 개인 프로젝트입니다.

## 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해주세요.

