# 서버 실행 가이드

## 현재 상태

✅ **백엔드 서버**: 실행 중 (포트 8000)
- API 엔드포인트: http://localhost:8000
- API 문서: http://localhost:8000/docs

❌ **프론트엔드**: Node.js가 설치되어 있지 않아 실행 불가

## 백엔드 접속 방법

브라우저에서 다음 주소로 접속하여 API를 테스트할 수 있습니다:

- **API 문서 (Swagger)**: http://localhost:8000/docs
- **대체 API 문서 (ReDoc)**: http://localhost:8000/redoc
- **카테고리 목록**: http://localhost:8000/api/categories

## 프론트엔드 실행을 위한 Node.js 설치

### macOS (Homebrew 사용)

```bash
brew install node
```

설치 후 확인:
```bash
node --version
npm --version
```

### 다른 설치 방법

1. **공식 웹사이트에서 설치**: https://nodejs.org/
   - LTS 버전 권장
   - 설치 후 터미널 재시작

2. **nvm (Node Version Manager) 사용**:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
nvm use --lts
```

## 프론트엔드 실행 방법

Node.js 설치 후:

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 http://localhost:3000 에서 실행됩니다.

## 샘플 데이터 추가 (선택사항)

백엔드에 샘플 데이터를 추가하려면:

```bash
cd backend
python3 init_data.py
```

이 스크립트는 다음을 생성합니다:
- 샘플 사용자 2명
- 구독 1개
- 샘플 활동 5개

## 문제 해결

### 백엔드 서버가 실행되지 않는 경우

```bash
cd backend
python3 main.py
```

또는:

```bash
cd backend
uvicorn main:app --reload
```

### 포트 충돌이 발생하는 경우

포트 8000이나 3000이 이미 사용 중인 경우, 다른 포트를 사용할 수 있습니다:

**백엔드:**
```bash
uvicorn main:app --port 8001
```

**프론트엔드:**
- `frontend/vite.config.js` 파일에서 포트 변경

## API 테스트 예시

### curl 명령어로 테스트

```bash
# 카테고리 목록
curl http://localhost:8000/api/categories

# 활동 목록
curl http://localhost:8000/api/activities

# 특정 활동 조회 (ID: 1)
curl http://localhost:8000/api/activities/1
```

## 현재 실행 중인 서버 종료

백엔드 서버를 종료하려면:

```bash
lsof -ti:8000 | xargs kill
```

또는 프로세스 ID를 찾아서 종료:
```bash
lsof -i :8000
kill <PID>
```

