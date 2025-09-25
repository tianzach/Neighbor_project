"""
Data models for the Multi-Vehicle Search API
"""

from .vehicle import Vehicle
from .listing import Listing
from .search_result import SearchResult

__all__ = ["Vehicle", "Listing", "SearchResult"]