# 📘 FastAPI API 경로 문서

> 이 문서는 FastAPI에서 기본적으로 제공하는 내장 경로(Documentation & OpenAPI)를 포함하며, 향후 사용자 정의 경로를 포함하는 문서로 확장될 수 있도록 설계되었습니다.

---

## 📂 기본 제공 경로

| 경로 | 메서드 | 설명 | 응답 형식 | 인증 필요 |
|------|--------|------|------------|------------|
| `/docs` | GET | Swagger UI (자동 문서화) | HTML | ❌ |
| `/redoc` | GET | ReDoc 문서화 뷰 | HTML | ❌ |
| `/openapi.json` | GET | OpenAPI 스펙 JSON 문서 | JSON | ❌ |

---

## 📂 사용자 정의 경로 (예시로 빈 항목 제공)

| 경로 | 메서드 | 설명 | 응답 형식 | 인증 필요 |
|------|--------|------|------------|------------|
| `/api/users` | GET | 사용자 목록 조회 | JSON | ✅ |
| `/api/login` | POST | 로그인 요청 | JSON | ❌ |
| `/api/items/{id}` | GET | 아이템 상세 조회 | JSON | ✅ |

---

## 📌 참고

- `/docs`, `/redoc`, `/openapi.json` 은 FastAPI의 `FastAPI()` 인스턴스 생성 시 기본적으로 활성화됩니다.
- 해당 경로를 비활성화하려면 앱 생성 시 아래와 같이 설정합니다:

```python
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
