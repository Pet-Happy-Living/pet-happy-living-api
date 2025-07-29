# API Client 사용 가이드

## 📋 개요

이 문서는 Pet Happy Living API에서 사용하는 공통 RESTful API 클라이언트의 사용법을 설명합니다.

## 🚀 기본 사용법

### 1. 클라이언트 초기화

```python
from app.api.common.client import APIClient

# 기본 초기화
client = APIClient("https://api.example.com")

# 커스텀 설정으로 초기화
client = APIClient(
    base_url="https://api.example.com",
    timeout=60,
    headers={"Authorization": "Bearer your-token"}
)
```

### 2. 비동기 컨텍스트 매니저 사용

```python
async def fetch_data():
    async with APIClient("https://api.example.com") as client:
        response = await client.get("users")
        return response
```

### 3. HTTP 메서드 사용

#### GET 요청
```python
# 기본 GET 요청
response = await client.get("users")

# 쿼리 파라미터와 함께
response = await client.get("users", params={"page": 1, "limit": 10})

# 커스텀 헤더와 함께
response = await client.get("users", headers={"X-Custom-Header": "value"})
```

#### POST 요청
```python
# JSON 데이터와 함께
data = {"name": "John", "email": "john@example.com"}
response = await client.post("users", data=data)

# 쿼리 파라미터와 함께
response = await client.post("users", data=data, params={"validate": "true"})
```

#### PUT 요청
```python
data = {"name": "John Updated", "email": "john.updated@example.com"}
response = await client.put("users/1", data=data)
```

#### DELETE 요청
```python
response = await client.delete("users/1")
```

#### PATCH 요청
```python
data = {"name": "John Updated"}
response = await client.patch("users/1", data=data)
```

## 🔧 에러 처리

### 1. 예외 타입

```python
from app.api.common.exceptions import (
    APIError, ClientError, ConnectionError, TimeoutError
)

try:
    response = await client.get("users")
except ClientError as e:
    print(f"클라이언트 에러: {e.status_code} - {e.message}")
except ConnectionError as e:
    print(f"연결 에러: {e.message}")
except TimeoutError as e:
    print(f"타임아웃 에러: {e.message}")
except APIError as e:
    print(f"API 에러: {e.status_code} - {e.message}")
```

### 2. 에러 정보 접근

```python
try:
    response = await client.get("users")
except APIError as e:
    print(f"상태 코드: {e.status_code}")
    print(f"에러 메시지: {e.message}")
    print(f"응답 데이터: {e.response_data}")
```

## 📊 실제 사용 예제

### 1. 서울시 동물병원 API 사용

```python
import os
from app.api.common.client import APIClient

async def fetch_pet_clinics(start: int = 1, end: int = 5):
    api_key = os.getenv("SEOUL_OPEN_API_KEY", "sample")
    base_url = "http://openapi.seoul.go.kr:8088"
    
    async with APIClient(base_url) as client:
        endpoint = f"{api_key}/json/LOCALDATA_020301/{start}/{end}/"
        response = await client.get(endpoint)
        return response
```

### 2. 외부 API 호출

```python
async def fetch_weather_data(city: str):
    async with APIClient("https://api.weatherapi.com") as client:
        params = {
            "key": "your-api-key",
            "q": city,
            "aqi": "no"
        }
        response = await client.get("v1/current.json", params=params)
        return response
```

## 🧪 테스트 작성

### 1. 단위 테스트

```python
import pytest
from unittest.mock import AsyncMock
from app.api.common.client import APIClient

@pytest.mark.asyncio
async def test_api_client_get():
    client = APIClient("http://test.api.com")
    client._client = AsyncMock()
    
    # Mock response
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    client._client.request.return_value = mock_response
    
    # Test
    result = await client.get("test")
    assert result == {"data": "test"}
```

### 2. 통합 테스트

```python
@pytest.mark.asyncio
async def test_real_api_call():
    async with APIClient("https://httpbin.org") as client:
        response = await client.get("json")
        assert "origin" in response
```

## 📈 로깅

API 클라이언트는 자동으로 요청과 응답을 로깅합니다:

```
INFO:app.api.common.client:Making GET request to https://api.example.com/users
INFO:app.api.common.client:Response status: 200
```

## ⚙️ 설정 옵션

### 1. 타임아웃 설정

```python
# 30초 타임아웃 (기본값)
client = APIClient("https://api.example.com", timeout=30)

# 60초 타임아웃
client = APIClient("https://api.example.com", timeout=60)
```

### 2. 기본 헤더 설정

```python
headers = {
    "Authorization": "Bearer your-token",
    "User-Agent": "MyApp/1.0",
    "Content-Type": "application/json"
}
client = APIClient("https://api.example.com", headers=headers)
```

### 3. URL 빌딩

```python
# 자동으로 URL을 조합합니다
client = APIClient("https://api.example.com")
# GET https://api.example.com/users
response = await client.get("users")

# 쿼리 파라미터 자동 인코딩
response = await client.get("users", params={"page": 1, "limit": 10})
# GET https://api.example.com/users?page=1&limit=10
```

## 🔍 디버깅

### 1. 요청/응답 로그 확인

```python
import logging

# 로그 레벨 설정
logging.basicConfig(level=logging.INFO)

async with APIClient("https://api.example.com") as client:
    response = await client.get("users")
    # 로그에서 요청/응답 정보 확인
```

### 2. 에러 디버깅

```python
try:
    response = await client.get("users")
except APIError as e:
    print(f"요청 URL: {e.url}")
    print(f"상태 코드: {e.status_code}")
    print(f"응답 데이터: {e.response_data}")
```

## 📚 추가 리소스

- [개발 진행 현황](../docs/development-progress.md)
- [테스트 가이드](../docs/test-guide.md)
- [API 문서](../docs/api_routes.md)

---

*마지막 업데이트: 2024-12-19* 