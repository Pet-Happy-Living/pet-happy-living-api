"""
Common RESTful API Client

This module provides a reusable HTTP client for making API requests.
"""

import httpx
import logging
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin, urlencode

from .exceptions import APIError, ClientError, ConnectionError, TimeoutError

logger = logging.getLogger(__name__)


class APIClient:
    """
    A reusable HTTP client for making API requests.
    
    This client provides a consistent interface for making HTTP requests
    with proper error handling, logging, and response processing.
    """
    
    def __init__(self, base_url: str, timeout: int = 30, 
                 headers: Optional[Dict[str, str]] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL for the API
            timeout: Request timeout in seconds
            headers: Default headers to include in all requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = headers or {}
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def _ensure_client(self):
        """Ensure the HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers
            )
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Build the full URL for the request.
        
        Args:
            endpoint: The API endpoint
            params: Query parameters
            
        Returns:
            The complete URL
        """
        url = urljoin(f"{self.base_url}/", endpoint.lstrip('/'))
        if params:
            url += f"?{urlencode(params)}"
        return url
    
    async def _make_request(self, method: str, endpoint: str, 
                           params: Optional[Dict[str, Any]] = None,
                           data: Optional[Dict[str, Any]] = None,
                           headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            headers: Additional headers
            
        Returns:
            Response data as dictionary
            
        Raises:
            APIError: For API-related errors
            ConnectionError: For connection errors
            TimeoutError: For timeout errors
        """
        await self._ensure_client()
        
        url = self._build_url(endpoint, params)
        request_headers = {**self.headers, **(headers or {})}
        
        logger.info(f"Making {method} request to {url}")
        
        try:
            response = await self._client.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=request_headers
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            # Handle different status codes
            if response.status_code >= 200 and response.status_code < 300:
                return response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise ClientError(
                    f"Client error: {response.status_code}",
                    status_code=response.status_code,
                    response_data=response.json() if response.content else {}
                )
            else:
                raise APIError(
                    f"Server error: {response.status_code}",
                    status_code=response.status_code,
                    response_data=response.json() if response.content else {}
                )
                
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")
            raise ConnectionError(f"Failed to connect to {url}: {e}")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")
            raise TimeoutError(f"Request timeout for {url}: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise APIError(f"Request failed for {url}: {e}")
        except (ClientError, APIError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise APIError(f"Unexpected error for {url}: {e}")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data
        """
        return await self._make_request("GET", endpoint, params=params, headers=headers)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                   params: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data
        """
        return await self._make_request("POST", endpoint, params=params, data=data, headers=headers)
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data
        """
        return await self._make_request("PUT", endpoint, params=params, data=data, headers=headers)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a DELETE request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data
        """
        return await self._make_request("DELETE", endpoint, params=params, headers=headers)
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    params: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make a PATCH request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data
        """
        return await self._make_request("PATCH", endpoint, params=params, data=data, headers=headers) 