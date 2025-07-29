# 테스트 가이드

## 📋 개요

이 문서는 Pet Happy Living API의 테스트 구조와 실행 방법을 설명합니다.

## 🏗️ 테스트 구조

```
tests/
├── __init__.py
├── conftest.py              # pytest 설정 및 fixtures
├── unit/                    # 단위 테스트
│   ├── __init__.py
│   └── test_api_client.py   # API 클라이언트 단위 테스트
└── integration/             # 통합 테스트
    ├── __init__.py
    └── test_pet_clinic_integration.py  # pet_clinic 통합 테스트
```

## 🧪 테스트 실행

### 1. 기본 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 상세 출력과 함께 실행
pytest -v

# 특정 테스트 파일 실행
pytest tests/unit/test_api_client.py

# 특정 테스트 함수 실행
pytest tests/unit/test_api_client.py::TestAPIClient::test_init
```

### 2. 테스트 결과 시각화

```bash
# 테스트 실행 및 결과 시각화
python scripts/run_tests.py
```

이 명령어는 다음을 수행합니다:
- 모든 테스트 실행
- 결과를 JSON 파일로 저장
- 시각화 차트 생성
- 상세한 테스트 리포트 생성

## 📊 테스트 결과 파일

테스트 실행 후 다음 파일들이 생성됩니다:

```
test_results/
├── test_results_YYYYMMDD_HHMMSS.json    # 테스트 결과 JSON
├── test_visualization_YYYYMMDD_HHMMSS.png  # 시각화 차트
└── test_report_YYYYMMDD_HHMMSS.md       # 상세 리포트
```

## 🧩 테스트 종류

### 1. 단위 테스트 (Unit Tests)

**위치**: `tests/unit/`

**목적**: 개별 함수나 클래스의 동작을 검증

**예제**:
```python
def test_api_client_init():
    """Test APIClient initialization."""
    client = APIClient("http://test.api.com")
    assert client.base_url == "http://test.api.com"
    assert client.timeout == 30
```

### 2. 통합 테스트 (Integration Tests)

**위치**: `tests/integration/`

**목적**: 여러 컴포넌트 간의 상호작용을 검증

**예제**:
```python
@pytest.mark.asyncio
async def test_pet_clinic_api_integration():
    """Test pet clinic API with real HTTP client."""
    async with APIClient("https://httpbin.org") as client:
        response = await client.get("json")
        assert "origin" in response
```

## 🔧 테스트 Fixtures

### 1. 기본 Fixtures

`tests/conftest.py`에 정의된 공통 fixtures:

```python
@pytest.fixture
def mock_api_client():
    """Create a mock API client for testing."""
    client = APIClient("http://test.api.com")
    client._client = AsyncMock()
    return client

@pytest.fixture
def sample_api_response():
    """Sample API response for testing."""
    return {
        "status": "success",
        "data": {"id": 1, "name": "Test Data"}
    }
```

### 2. Fixture 사용법

```python
def test_with_fixture(mock_api_client, sample_api_response):
    """Test using fixtures."""
    # mock_api_client와 sample_api_response 사용
    pass
```

## 📈 테스트 커버리지

### 1. 커버리지 측정

```bash
# pytest-cov 설치
pip install pytest-cov

# 커버리지 측정
pytest --cov=app tests/

# HTML 리포트 생성
pytest --cov=app --cov-report=html tests/
```

### 2. 커버리지 리포트

HTML 리포트는 `htmlcov/` 디렉토리에 생성됩니다.

## 🚨 테스트 디버깅

### 1. 실패한 테스트 디버깅

```bash
# 실패한 테스트만 실행
pytest --lf

# 실패한 테스트의 상세 정보
pytest -vv --tb=long

# 디버거 모드로 실행
pytest --pdb
```

### 2. 로그 확인

```python
import logging

# 테스트에서 로그 확인
logging.basicConfig(level=logging.DEBUG)
```

## 📝 테스트 작성 가이드

### 1. 테스트 함수 명명 규칙

```python
def test_function_name():
    """Test description."""
    pass

def test_class_name_method_name():
    """Test description."""
    pass
```

### 2. 테스트 구조

```python
def test_example():
    """Test description."""
    # Arrange (준비)
    client = APIClient("http://test.api.com")
    
    # Act (실행)
    result = client._build_url("test")
    
    # Assert (검증)
    assert result == "http://test.api.com/test"
```

### 3. 비동기 테스트

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    async with APIClient("http://test.api.com") as client:
        response = await client.get("test")
        assert response is not None
```

## 🔍 Mock 사용법

### 1. HTTP 요청 Mock

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_mock_http_request():
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        # 테스트 실행
        result = await fetch_data()
        assert result == {"data": "test"}
```

### 2. 환경 변수 Mock

```python
from unittest.mock import patch

def test_with_env_vars():
    with patch.dict(os.environ, {"API_KEY": "test_key"}):
        # 테스트 실행
        pass
```

## 📊 테스트 결과 해석

### 1. 성공한 테스트

```
✅ test_api_client_init PASSED
✅ test_api_client_get_request PASSED
```

### 2. 실패한 테스트

```
❌ test_api_client_error_handling FAILED
    assert 400 == 404
    +  where 400 = <ClientError object>.status_code
```

### 3. 건너뛴 테스트

```
⏭️ test_requires_network SKIPPED
    reason: Network not available
```

## 🚀 CI/CD 통합

### 1. GitHub Actions 예제

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python scripts/run_tests.py
```

## 📚 추가 리소스

- [pytest 공식 문서](https://docs.pytest.org/)
- [pytest-asyncio 문서](https://pytest-asyncio.readthedocs.io/)
- [API Client 사용 가이드](./api-client-guide.md)
- [개발 진행 현황](./development-progress.md)

---

*마지막 업데이트: 2024-12-19* 