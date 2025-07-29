"""
Custom exceptions for API client operations.
"""

from typing import Optional, Dict, Any


class APIError(Exception):
    """Base exception for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)


class ClientError(APIError):
    """Exception raised for client-side errors (4xx status codes)."""
    pass


class ValidationError(APIError):
    """Exception raised for validation errors."""
    pass


class ConnectionError(APIError):
    """Exception raised for connection-related errors."""
    pass


class TimeoutError(APIError):
    """Exception raised for timeout errors."""
    pass 