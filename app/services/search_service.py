"""
Search service for vehicle storage search
"""

from typing import List
from ..models.vehicle import Vehicle
from ..models.vehicle_unit import VehicleUnit
from ..models.listing import Listing
from ..models.search_result import SearchResult
from ..utils.bin_packing import BinPackingAlgorithm
from .listing_service import ListingService
from ..config.settings import settings


class SearchService:
    """
    Service for handling vehicle storage search operations
    """
    
    def __init__(self, listing_service: ListingService):
        self.listing_service = listing_service
    
    def validate_vehicles(self, vehicles: List[Vehicle]) -> None:
        """
        Validate vehicle input
        
        Args:
            vehicles: List of vehicles to validate
            
        Raises:
            ValueError: If validation fails
        """
        if not vehicles:
            raise ValueError("At least one vehicle is required")
        
        total_quantity = sum(vehicle.quantity for vehicle in vehicles)
        if total_quantity > settings.max_vehicles_per_request:
            raise ValueError(f"Total vehicle quantity cannot exceed {settings.max_vehicles_per_request}")
        
        if total_quantity == 0:
            raise ValueError("At least one vehicle with quantity > 0 is required")
    
    def convert_vehicles_to_units(self, vehicles: List[Vehicle]) -> List[VehicleUnit]:
        """
        Convert vehicles to individual vehicle units
        
        Args:
            vehicles: List of vehicles
            
        Returns:
            List[VehicleUnit]: List of individual vehicle units
        """
        vehicle_units = []
        for vehicle in vehicles:
            vehicle_units.extend(vehicle.to_individual_vehicles())
        return vehicle_units
    
    def search_locations(self, vehicles: List[Vehicle]) -> List[SearchResult]:
        """
        Search for storage locations that can accommodate the given vehicles
        
        Args:
            vehicles: List of vehicles to store
            
        Returns:
            List[SearchResult]: List of search results sorted by price
            
        Raises:
            ValueError: If input validation fails
        """
        # Validate input
        self.validate_vehicles(vehicles)
        
        # Convert to vehicle units
        vehicle_units = self.convert_vehicles_to_units(vehicles)
        
        # Get all location groups
        location_groups = self.listing_service.get_listings_by_location()
        
        results = []
        
        # Check each location
        for location_id, location_listings in location_groups.items():
            # Check if vehicles can fit in this location
            if BinPackingAlgorithm.can_fit_vehicles(vehicle_units, location_listings):
                # Find optimal combination for this location
                optimal_listings = BinPackingAlgorithm.find_optimal_combination(
                    vehicle_units, location_listings
                )
                
                if optimal_listings:
                    total_price = BinPackingAlgorithm.calculate_total_price(optimal_listings)
                    listing_ids = [listing.id for listing in optimal_listings]
                    
                    results.append(SearchResult(
                        location_id=location_id,
                        listing_ids=listing_ids,
                        total_price_in_cents=total_price
                    ))
        
        # Sort by total price (ascending)
        results.sort(key=lambda x: x.total_price_in_cents)
        
        return results
    
    def get_search_statistics(self, vehicles: List[Vehicle]) -> dict:
        """
        Get statistics about the search operation
        
        Args:
            vehicles: List of vehicles
            
        Returns:
            dict: Search statistics
        """
        vehicle_units = self.convert_vehicles_to_units(vehicles)
        location_groups = self.listing_service.get_listings_by_location()
        
        total_locations = len(location_groups)
        feasible_locations = 0
        total_listings = sum(len(listings) for listings in location_groups.values())
        
        for location_listings in location_groups.values():
            if BinPackingAlgorithm.can_fit_vehicles(vehicle_units, location_listings):
                feasible_locations += 1
        
        return {
            "total_vehicles": len(vehicle_units),
            "total_locations": total_locations,
            "feasible_locations": feasible_locations,
            "total_listings": total_listings,
            "feasibility_rate": feasible_locations / total_locations if total_locations > 0 else 0
        }