"""
Search controller for handling API requests
"""

from fastapi import HTTPException, status
from typing import List
from ..models.vehicle import Vehicle
from ..models.search_result import SearchResult
from ..services.search_service import SearchService
from ..services.listing_service import ListingService
from ..config.settings import settings


class SearchController:
    """
    Controller for handling search-related API requests
    """
    
    def __init__(self):
        self.listing_service = ListingService()
        self.search_service = SearchService(self.listing_service)
    
    async def search_vehicles(self, vehicles: List[Vehicle]) -> List[SearchResult]:
        """
        Handle vehicle search request
        
        Args:
            vehicles: List of vehicles to search for
            
        Returns:
            List[SearchResult]: Search results
            
        Raises:
            HTTPException: If search fails
        """
        try:
            results = self.search_service.search_locations(vehicles)
            return results
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    async def get_search_statistics(self, vehicles: List[Vehicle]) -> dict:
        """
        Get search statistics
        
        Args:
            vehicles: List of vehicles
            
        Returns:
            dict: Search statistics
        """
        try:
            return self.search_service.get_search_statistics(vehicles)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting statistics: {str(e)}"
            )