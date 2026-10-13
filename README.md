# INTJ-비서AI

React + Spring Boot + LangGraph 개인 일정 비서.

## 포트

- frontend: `5173`
- backend: `8080`
- ai-agent: `8000`
- PostgreSQL: `localhost:4000` / DB `intj_ai`

## 사전 준비

- JDK 21 (`JAVA_HOME=C:\Users\user\.jdks\ms-21.0.12`)
- Node 24 + npm
- Python 3.12
- 실행 중인 PostgreSQL 컨테이너
- 루트에 `.env` 생성 (`cp .env.example .env` 후 `DB_PASSWORD` 입력)

## 실행

### backend

```powershell
cd backend
$env:JAVA_HOME = "C:\Users\user\.jdks\ms-21.0.12"
$env:DB_PASSWORD = "your-db-password"
.\gradlew.bat bootRun
```

- Health: http://localhost:8080/api/health
- Swagger: http://localhost:8080/swagger-ui.html

### frontend

```bash
cd frontend
npm install
npm run dev
```

http://localhost:5173

### ai-agent

```powershell
cd ai-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

http://localhost:8000/health

## 아직 하지 않은 것

- CORS (React + Spring 기동 후 재확인)
- JWT
- 엔티티 / Flyway DDL
- Docker Compose
