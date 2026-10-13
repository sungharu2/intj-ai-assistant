# AGENTS.md — INTJ-비서AI

> 이 문서는 다른 세션이 프로젝트 Context를 빠르게 따라잡기 위한 단일 진입점이다.
> 세부 실행 방법은 `README.md`, 초기 환경 변수는 `.env.example` 참고.

## 프로젝트 한 줄 소개

React + Spring Boot + LangGraph 기반 **개인 일정 관리 서비스 + AI 비서**.
사용자가 일정을 직접 관리하고, AI가 일정/할 일을 분석해 생성·수정·재조정을 지원한다.

## 핵심 목표

- 학습 목표인 **React + Spring을 중심**에 두고, LangGraph(AI)와 Discord(알림)를 명확한 역할로 배치한다.
- **"AI가 없어도 정상 동작하는 일정 관리 시스템"**을 Spring에서 먼저 완성한다.
- AI가 DB를 직접 조작하지 않고 **Spring이 정의한 Tool/API를 통해서만** 일정 데이터에 접근한다.
- 사용자가 질문해야만 동작하는 챗봇이 아니라, 스케줄러가 **능동적으로 일정을 분석·알림**하는 비서를 목표로 한다.

## 아키텍처 / 역할 분리

```
사용자
  ├── React (Calendar / Dashboard / AI Chat)
  ▼
Spring Boot  ── 일정·Todo 관리, 검증, 충돌 처리, Scheduler, AI Agent 연동 (서비스의 중심)
  ├──▼ LangGraph ── 의도 분석, 일정 분석, Tool Calling, 재조정안 생성, State/Context 관리 → LLM
  └──▼ Discord Webhook ── 일정/추천/분석 결과 알림
```

| 계층 | 책임 |
|------|------|
| React (`frontend`) | 일정 관리 UI, Calendar, Dashboard, AI Chat, 추천 결과 확인 |
| Spring Boot (`backend`) | 비즈니스 로직의 중심. 일정/Todo 관리, 데이터 관리, 일정 검증, 충돌 처리, Scheduler, AI 연동 |
| LangGraph (`ai-agent`) | AI 판단과 Agent Workflow. 의도 분석, Tool Calling, 재조정안 생성 |
| Discord Webhook | 결과 Notification 채널 |

**핵심 원칙**: 직접 관리(React)와 AI 관리(LangGraph)는 **동일한 일정 데이터**를 사용한다. 분리하지 않고 하나의 일정 시스템 안에서 통합한다.

## 기술 스택 (실제 코드 기준)

- **Frontend** `frontend/`: React 19, TypeScript 6, Vite 8, oxlint
- **Backend** `backend/`: Java 21, Spring Boot 3.4.13 (web, jdbc, validation, flyway), PostgreSQL, springdoc-openapi(Swagger) 2.8.17. 빌드: Gradle wrapper 8.14.3
- **AI Agent** `ai-agent/`: Python + FastAPI, LangGraph, LangChain. LLM fallback 순서: **Gemini → Groq → Ollama**
- **DB**: PostgreSQL
- **Notification**: Discord Webhook (REST)
- **IDE/Agent**: VSCode / Command Code

## 저장소 구조

```
intj-ai-assistant/
├── frontend/        # React (Vite) — 포트 5173
├── backend/         # Spring Boot (Gradle) — 포트 8080, DB 마이그레이션은 Flyway (db/migration)
├── ai-agent/        # FastAPI + LangGraph — 포트 8000
│   └── app/         # main.py(FastAPI 진입), llm.py(provider 선택), graph/state.py(AgentState)
├── .env.example     # 환경 변수 템플릿
└── README.md
```

## 포트 / 실행

| 서비스 | 포트 | 실행 |
|--------|------|------|
| frontend | 5173 | `cd frontend && npm install && npm run dev` |
| backend | 8080 | `cd backend && .\gradlew.bat bootRun` (JDK 21, `DB_PASSWORD` 필요) |
| ai-agent | 8000 | `cd ai-agent && uvicorn app.main:app --reload --port 8000` |
| PostgreSQL | 4000 | DB `intj_ai` (컨테이너) |

- backend Health: `GET /api/health`, Swagger: `/swagger-ui.html`
- ai-agent Health: `GET /health` (현재 연동된 LLM provider 상태와 AgentState 키를 반환)
- **`.env`는 루트에 생성** (`.env.example` 복사 후 `DB_PASSWORD` 입력). 커밋하지 않는다.

## 현재 구현 상태

- 스캐폴딩 완료: 3개 서비스 디렉터리, FastAPI health, `AgentState` 정의, Spring 설정, 프론트 Vite 세팅
- **아직 하지 않은 것**: CORS(frontend↔backend), JWT, 엔티티/Flyway DDL, Docker Compose, 실제 Tool Calling / 일정 API 연동
