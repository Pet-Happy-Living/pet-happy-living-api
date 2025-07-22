# 🐶 Pet Happy Recommendation API – 프로젝트 운영 및 실행 환경 가이드

**팀명**: 미정
**작성자**: 정규호  
**작성 날짜**: 2025-07-20  
**문서 버전**: v1.1  

---

## 📋 목차

- [🐶 Pet Happy Recommendation API – 프로젝트 운영 및 실행 환경 가이드](#-pet-happy-recommendation-api--프로젝트-운영-및-실행-환경-가이드)
  - [📋 목차](#-목차)
  - [📌 프로젝트 개요](#-프로젝트-개요)
  - [⚙️ 환경 구성 개요](#️-환경-구성-개요)
  - [🐳 Docker Compose 분리 구조](#-docker-compose-분리-구조)
    - [📁 구조 예시](#-구조-예시)
    - [✅ 실행 예시](#-실행-예시)
  - [🌍 환경 변수 파일(.env) 분리 관리](#-환경-변수-파일env-분리-관리)
    - [`.env.dev`](#envdev)
    - [`.env.prod`](#envprod)
  - [🧠 FastAPI 실행 시 SSH Tunnel 조건부 분기](#-fastapi-실행-시-ssh-tunnel-조건부-분기)
  - [🚀 실행 스크립트(sh 파일) 구성 및 사용법](#-실행-스크립트sh-파일-구성-및-사용법)
    - [📁 위치](#-위치)
    - [start-dev.sh](#start-devsh)
    - [start-prod.sh](#start-prodsh)
  - [📣 빌드가 필요한 경우](#-빌드가-필요한-경우)
  - [📝 로깅 및 디버깅 가이드](#-로깅-및-디버깅-가이드)
  - [✅ 요약](#-요약)

---

## 📌 프로젝트 개요

본 프로젝트는 지역별 반려동물 행복도를 분석하고 추천 주거지를 제안하는 **Pet Happy Recommendation API**입니다.  
FastAPI + PostgreSQL + Redis + SSH Tunnel 구성으로, EC2 서버 원격 PostgreSQL에 개발 환경에서만 터널링 접속합니다.

---

## ⚙️ 환경 구성 개요

| 환경 | 목적 | 실행 포트 | SSH 터널 | .env 파일 |
|------|------|-----------|----------|-----------|
| dev  | 개발자 로컬 실행 | 8000 | 활성화 | `.env.dev` |
| prod | 실제 운영 환경  | 8000 (or Docker 설정값) | 비활성화 | `.env.prod` |

---

## 🐳 Docker Compose 분리 구조

Docker Compose는 공통 설정(`base`)과 환경별 설정(`dev`, `prod`)로 분리됩니다.

### 📁 구조 예시

```
project-root/
├── docker-compose.base.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
```

### ✅ 실행 예시

```bash
./scripts/start-dev.sh
./scripts/start-dev.sh --build
./scripts/start-prod.sh
./scripts/start-prod.sh --build
```

---

## 🌍 환경 변수 파일(.env) 분리 관리

`.env` 파일은 환경마다 다르게 사용하며 `--env-file`로 주입됩니다.

### `.env.dev`

```env
ENV=dev
SSH_HOST=ec2-xx.ap-northeast-2.compute.amazonaws.com
SSH_USER=ubuntu
PRIVATE_KEY_PATH=./key.pem
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASS=secret
```

### `.env.prod`

```env
ENV=prod
POSTGRES_HOST=db.internal
POSTGRES_PORT=5432
POSTGRES_USER=prod_user
POSTGRES_PASS=prod_password
```

---

## 🧠 FastAPI 실행 시 SSH Tunnel 조건부 분기

```python
@app.on_event("startup")
def start_ssh_tunnel():
    global tunnel
    if settings.ENV == "dev":
        tunnel = SSHTunnelForwarder(
            (settings.SSH_HOST, settings.SSH_PORT),
            ssh_username=settings.SSH_USER,
            ssh_private_key=settings.PRIVATE_KEY_PATH,
            remote_bind_address=(settings.POSTGRES_HOST, settings.POSTGRES_PORT),
            local_bind_address=("127.0.0.1", 15432)
        )
        tunnel.start()
    else:
        logger.info("✅ 운영 환경으로 SSH Tunnel은 비활성화됩니다.")
```

> `shutdown` 시 `tunnel.stop()` 실행 필요

---

## 🚀 실행 스크립트(sh 파일) 구성 및 사용법

### 📁 위치

```
scripts/
├── start-dev.sh
├── start-prod.sh
```

### start-dev.sh

- `--build` 옵션 유무 확인
- 안내 메시지 출력
- Docker Compose dev 실행

### start-prod.sh

- `--build` 옵션 유무 확인
- 안내 메시지 출력
- Docker Compose prod 실행

> 변경사항 반영 시 반드시 `--build` 옵션 사용

---

## 📣 빌드가 필요한 경우

다음의 경우 반드시 `--build` 필요:

- `requirements.txt` 수정
- `Dockerfile` 수정
- 의존성 추가/삭제
- `docker-compose.*.yml` 변경

```bash
./scripts/start-dev.sh --build
./scripts/start-prod.sh --build
```

---

## 📝 로깅 및 디버깅 가이드

- `.env`에 `DEBUG=true` 설정 시 FastAPI 디버그 모드
- `logger`로 SSH 연결 성공/실패 및 서버 상태 확인 가능

---

## ✅ 요약

| 항목 | 내용 |
|------|------|
| Docker 구성 | base + dev/prod 분리 |
| 환경 변수 관리 | `.env.dev`, `.env.prod` |
| SSH Tunnel 분기 | 개발 환경에서만 활성화 |
| 실행 방식 | `start-dev.sh`, `start-prod.sh` |
| 빌드 여부 제어 | `--build` 명시적 사용 |
