"""
Unit tests for API Client
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch
from app.api.common.client import APIClient
from app.api.common.exceptions import APIError, ClientError, ConnectionError, TimeoutError


class TestAPIClient:
    """Test cases for APIClient class."""
    
    def test_init(self):
        """Test APIClient initialization."""
        client = APIClient("http://test.api.com")
        assert client.base_url == "http://test.api.com"
        assert client.timeout == 30
        assert client.headers == {}
        assert client._client is None
    
    def test_init_with_custom_params(self):
        """Test APIClient initialization with custom parameters."""
        headers = {"Authorization": "Bearer token"}
        client = APIClient("http://test.api.com", timeout=60, headers=headers)
        assert client.base_url == "http://test.api.com"
        assert client.timeout == 60
        assert client.headers == headers
    
    def test_build_url(self):
        """Test URL building functionality."""
        client = APIClient("http://test.api.com")
        
        # Test basic URL building
        url = client._build_url("endpoint")
        assert url == "http://test.api.com/endpoint"
        
        # Test URL with parameters
        params = {"key": "value", "page": 1}
        url = client._build_url("endpoint", params)
        assert "http://test.api.com/endpoint?" in url
        assert "key=value" in url
        assert "page=1" in url
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager functionality."""
        async with APIClient("http://test.api.com") as client:
            assert client._client is not None
            assert isinstance(client._client, httpx.AsyncClient)
        
        # Client should be closed after context exit
        assert client._client is None
    
    @pytest.mark.asyncio
    async def test_get_request_success(self, mock_api_client, sample_api_response):
        """Test successful GET request."""
        # Mock the response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value=sample_api_response)
        mock_response.content = b'{"status": "success"}'
        
        mock_api_client._client.request = AsyncMock(return_value=mock_response)
        
        # Make request
        result = await mock_api_client.get("test-endpoint")
        
        # Verify request was made correctly
        mock_api_client._client.request.assert_called_once()
        call_args = mock_api_client._client.request.call_args
        assert call_args[1]["method"] == "GET"
        assert "test-endpoint" in call_args[1]["url"]
        
        # Verify response
        assert result == sample_api_response
    
    @pytest.mark.asyncio
    async def test_post_request_success(self, mock_api_client, sample_api_response):
        """Test successful POST request."""
        # Mock the response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value=sample_api_response)
        mock_response.content = b'{"status": "success"}'
        
        mock_api_client._client.request = AsyncMock(return_value=mock_response)
        
        # Test data
        data = {"name": "test", "value": 123}
        
        # Make request
        result = await mock_api_client.post("test-endpoint", data=data)
        
        # Verify request was made correctly
        mock_api_client._client.request.assert_called_once()
        call_args = mock_api_client._client.request.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["json"] == data
        
        # Verify response
        assert result == sample_api_response
    
    @pytest.mark.asyncio
    async def test_client_error_handling(self, mock_api_client):
        """Test client error (4xx) handling."""
        # Mock error response
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json = AsyncMock(return_value={"error": "Bad Request"})
        mock_response.content = b'{"error": "Bad Request"}'
        
        mock_api_client._client.request = AsyncMock(return_value=mock_response)
        
        # Should raise ClientError
        with pytest.raises(ClientError) as exc_info:
            await mock_api_client.get("test-endpoint")
        
        assert exc_info.value.status_code == 400
        assert "Client error: 400" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_server_error_handling(self, mock_api_client):
        """Test server error (5xx) handling."""
        # Mock error response
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_response.json = AsyncMock(return_value={"error": "Internal Server Error"})
        mock_response.content = b'{"error": "Internal Server Error"}'
        
        mock_api_client._client.request = AsyncMock(return_value=mock_response)
        
        # Should raise APIError
        with pytest.raises(APIError) as exc_info:
            await mock_api_client.get("test-endpoint")
        
        assert exc_info.value.status_code == 500
        assert "Server error: 500" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_connection_error_handling(self, mock_api_client):
        """Test connection error handling."""
        # Mock connection error
        mock_api_client._client.request.side_effect = httpx.ConnectError("Connection failed")
        
        # Should raise ConnectionError
        with pytest.raises(ConnectionError) as exc_info:
            await mock_api_client.get("test-endpoint")
        
        assert "Failed to connect" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_timeout_error_handling(self, mock_api_client):
        """Test timeout error handling."""
        # Mock timeout error
        mock_api_client._client.request.side_effect = httpx.TimeoutException("Request timeout")
        
        # Should raise TimeoutError
        with pytest.raises(TimeoutError) as exc_info:
            await mock_api_client.get("test-endpoint")
        
        assert "Request timeout" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_all_http_methods(self, mock_api_client, sample_api_response):
        """Test all HTTP methods."""
        # Mock response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_response.content = b'{"status": "success"}'
        
        mock_api_client._client.request.return_value = mock_response
        
        # Test all methods
        methods = ["get", "post", "put", "delete", "patch"]
        test_data = {"test": "data"}
        
        for method in methods:
            mock_api_client._client.request.reset_mock()
            
            if method in ["post", "put", "patch"]:
                await getattr(mock_api_client, method)("test-endpoint", data=test_data)
            else:
                await getattr(mock_api_client, method)("test-endpoint")
            
            # Verify method was called
            call_args = mock_api_client._client.request.call_args
            assert call_args[1]["method"].upper() == method.upper() 