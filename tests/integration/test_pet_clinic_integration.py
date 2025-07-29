"""
Integration tests for Pet Clinic API with common client
"""

import pytest
import os
from unittest.mock import patch, AsyncMock
from app.api.v1.endpoints.pet_clinic import load_pet_clinics
from app.api.common.client import APIClient
from app.api.common.exceptions import APIError


class TestPetClinicIntegration:
    """Integration tests for Pet Clinic API."""
    
    @pytest.mark.asyncio
    async def test_load_pet_clinics_with_mock_api(self):
        """Test load_pet_clinics function with mocked API response."""
        # Mock API response
        mock_response = {
            "LOCALDATA_020301": {
                "row": [
                    {
                        "OPNSFTEAMCODE": "TEST001",
                        "MGTNO": "1234567890",
                        "APVPERMYMD": "20240101",
                        "APVCANCELYMD": "",
                        "TRDSTATEGBN": "01",
                        "TRDSTATENM": "영업",
                        "DTLSTATEGBN": "01",
                        "DTLSTATENM": "영업",
                        "DCBYMD": "",
                        "CLGSTDT": "",
                        "CLGENDDT": "",
                        "ROPNYMD": "20240101",
                        "SITETEL": "02-1234-5678",
                        "SITEAREA": "100.5",
                        "SITEPOSTNO": "12345",
                        "SITEWHLADDR": "서울시 강남구 테스트로 123",
                        "RDNWHLADDR": "서울시 강남구 테스트로 123",
                        "RDNPOSTNO": "12345",
                        "BPLCNM": "테스트 동물병원",
                        "LASTMODTS": "20240101120000",
                        "UPDATEGBN": "I",
                        "UPDATEDT": "20240101",
                        "UPTAENM": "테스트",
                        "X": "127.123456",
                        "Y": "37.123456",
                        "LINDJOBGBNNM": "동물병원",
                        "LINDPRCBGBNNM": "동물병원",
                        "LINDSEQNO": "001",
                        "RGTMBDSNO": "1234567890",
                        "TOTEPNUM": "5"
                    }
                ]
            }
        }
        
        # Mock environment variable
        with patch.dict(os.environ, {"SEOUL_OPEN_API_KEY": "test_key"}):
            # Mock httpx.AsyncClient
            with patch("httpx.AsyncClient") as mock_client_class:
                mock_client = AsyncMock()
                mock_response_obj = AsyncMock()
                mock_response_obj.json.return_value = mock_response
                mock_client.get = AsyncMock(return_value=mock_response_obj)
                mock_client_class.return_value.__aenter__.return_value = mock_client
                
                # Mock database session
                with patch("app.api.v1.endpoints.pet_clinic.get_db") as mock_get_db:
                    mock_db = AsyncMock()
                    mock_get_db.return_value = mock_db
                    
                    # Call the function
                    result = await load_pet_clinics(start=1, end=1)
                    
                    # Verify API call was made
                    mock_client.get.assert_called_once()
                    call_args = mock_client.get.call_args
                    assert "openapi.seoul.go.kr:8088" in call_args[0][0]
                    assert "test_key" in call_args[0][0]
                    
                    # Verify database operations
                    assert mock_db.execute.called
                    assert mock_db.commit.called
                    
                    # Verify result
                    assert len(result) == 1
                    assert result[0].bplc_nm == "테스트 동물병원"
                    assert result[0].mgt_no == "1234567890"
    
    @pytest.mark.asyncio
    async def test_api_client_with_real_endpoint(self):
        """Test API client with a real endpoint (using httpbin for testing)."""
        async with APIClient("https://httpbin.org") as client:
            # Test GET request
            response = await client.get("json")
            assert "slideshow" in response
            assert "author" in response["slideshow"]
            
            # Test POST request
            test_data = {"test": "data", "number": 123}
            response = await client.post("post", data=test_data)
            assert response["json"] == test_data
            assert response["url"] == "https://httpbin.org/post"
    
    @pytest.mark.asyncio
    async def test_api_client_error_handling(self):
        """Test API client error handling with non-existent endpoint."""
        async with APIClient("https://httpbin.org") as client:
            # Test 404 error
            with pytest.raises(APIError) as exc_info:
                await client.get("status/404")
            
            assert exc_info.value.status_code == 404
            
            # Test 500 error
            with pytest.raises(APIError) as exc_info:
                await client.get("status/500")
            
            assert exc_info.value.status_code == 500
    
    @pytest.mark.asyncio
    async def test_api_client_with_headers(self):
        """Test API client with custom headers."""
        headers = {"User-Agent": "TestClient/1.0", "X-Test-Header": "test-value"}
        
        async with APIClient("https://httpbin.org", headers=headers) as client:
            response = await client.get("headers")
            
            # Verify headers were sent
            assert response["headers"]["User-Agent"] == "TestClient/1.0"
            assert response["headers"]["X-Test-Header"] == "test-value"
    
    @pytest.mark.asyncio
    async def test_api_client_with_query_params(self):
        """Test API client with query parameters."""
        async with APIClient("https://httpbin.org") as client:
            params = {"param1": "value1", "param2": "value2"}
            response = await client.get("get", params=params)
            
            # Verify parameters were sent
            assert response["args"]["param1"] == "value1"
            assert response["args"]["param2"] == "value2"
    
    @pytest.mark.asyncio
    async def test_api_client_timeout(self):
        """Test API client timeout handling."""
        # Use a slow endpoint to test timeout
        async with APIClient("https://httpbin.org", timeout=1) as client:
            # This should timeout
            with pytest.raises(TimeoutError):
                await client.get("delay/5") 