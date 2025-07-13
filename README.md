# 🐾 Pet Happy Living API

**A FastAPI-based microservice for recommending pet-friendly residential areas, built on Kubernetes and ready for ML/LLM/IoT extensions.**

---

## 🗂️ Project Overview

**Pet Happy Living API**는 반려동물의 행복한 삶을 위한 거주 지역을 추천하는 웹 서비스의 핵심 API 서버입니다. 도시 환경 데이터, 공공 인프라, 소음·녹지·밀집도 등 다양한 요소를 분석하여 반려동물과 보호자에게 최적의 거주지를 추천하는 AI 기반 마이크로서비스입니다.

---

## 🛠️ Tech Stack

| Layer            | Tech                             |
|------------------|----------------------------------|
| Language         | Python 3.10                      |
| Framework        | FastAPI                         |
| Web Server       | Uvicorn (ASGI)                   |
| Containerization | Docker, Kubernetes (K8s)         |
| DB               | PostgreSQL, Redis                |
| Infra            | AWS EC2                          |
| Docs & Test      | OpenAPI, Swagger UI, curl        |

---

## 📁 Project Structure

```
pet-happy-api/
├── app/
│   ├── main.py                # FastAPI 엔트리포인트
│   ├── api/
│   │   └── endpoints.py       # API 엔드포인트 (e.g., /health)
│   └── core/
│       └── config.py          # 설정 및 환경변수 로딩
├── requirements.txt           # Python 패키지 목록
├── Dockerfile                 # Docker 이미지 설정
└── README.md                  # 프로젝트 설명 문서
```

---

## 🚀 Getting Started

### 1️⃣ Clone this repo

```bash
git clone https://github.com/<your-username>/pet-happy-living-api.git
cd pet-happy-living-api
```

### 2️⃣ Build & Run with Docker

```bash
docker build -t pet-happy-api .
docker run -d -p 8000:8000 pet-happy-api
```

접속: [http://localhost:8000/health](http://localhost:8000/health)

### 3️⃣ Kubernetes 배포

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## ✅ Health Check

```bash
curl http://<your-ip>/health
# {"status": "ok"}
```

---

## 📈 Future Extensions(예시)

- 🧠 LLM + RAG 기반 거주지 질문응답
- 📊 데이터 분석 기반 기회비용 지표 제공
- 📡 IoT 센서 연동 (소음, 온도, 산책량 등)
- 🐶 사용자 기반 반려동물 특성 맞춤 추천

---

## 📝 License

MIT License
