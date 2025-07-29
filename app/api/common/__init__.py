"""
Common API Client Package

This package provides reusable RESTful API client components for the Pet Happy Living API.
"""

from .client import APIClient
from .exceptions import APIError, ClientError, ValidationError

__all__ = [
    "APIClient",
    "APIError", 
    "ClientError",
    "ValidationError"
]

__version__ = "1.0.0" 