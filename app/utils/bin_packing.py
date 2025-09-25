"""
Bin packing algorithm utilities
"""

from typing import List, Set, Tuple, Optional
from ..models.listing import Listing
from ..models.vehicle_unit import VehicleUnit


class BinPackingAlgorithm:
    """
    Implements bin packing algorithm for vehicle storage optimization
    """
    
    @staticmethod
    def can_fit_vehicles(vehicles: List[VehicleUnit], listings: List[Listing]) -> bool:
        """
        Check if a list of vehicles can fit in a list of listings using bin packing algorithm
        
        Args:
            vehicles: List of vehicle units to fit
            listings: List of available listings
            
        Returns:
            bool: True if all vehicles can fit, False otherwise
        """
        if not vehicles or not listings:
            return False
            
        # Sort vehicles by area (descending) for better packing
        sorted_vehicles = sorted(vehicles, key=lambda x: x.area, reverse=True)
        
        # Sort listings by area (ascending) to use smaller spaces first
        available_listings = sorted(listings, key=lambda x: x.area)
        
        # Track which listings are used
        used_listings = set()
        
        # Try to fit each vehicle
        for vehicle in sorted_vehicles:
            fitted = False
            for i, listing in enumerate(available_listings):
                if i in used_listings:
                    continue
                
                # Check if vehicle fits in listing
                if vehicle.fits_in(listing):
                    used_listings.add(i)
                    fitted = True
                    break
            
            if not fitted:
                return False
        
        return True
    
    @staticmethod
    def find_optimal_combination(vehicles: List[VehicleUnit], 
                               listings: List[Listing]) -> List[Listing]:
        """
        Find the optimal combination of listings for the given vehicles
        
        Args:
            vehicles: List of vehicle units to fit
            listings: List of available listings
            
        Returns:
            List[Listing]: Optimal combination of listings, empty if no solution
        """
        if not vehicles or not listings:
            return []
        
        # Sort vehicles by area descending for better packing
        sorted_vehicles = sorted(vehicles, key=lambda x: x.area, reverse=True)
        
        # Sort listings by price per unit area (ascending) for optimal cost
        sorted_listings = sorted(listings, 
                               key=lambda x: x.price_per_unit_area)
        
        # Use backtracking to find optimal combination
        used_listings = []
        used_indices = set()
        
        def backtrack(vehicle_index: int) -> bool:
            """Recursive backtracking function"""
            if vehicle_index >= len(sorted_vehicles):
                return True
            
            vehicle = sorted_vehicles[vehicle_index]
            
            for i, listing in enumerate(sorted_listings):
                if i in used_indices:
                    continue
                
                # Check if vehicle fits in listing
                if vehicle.fits_in(listing):
                    used_indices.add(i)
                    used_listings.append(listing)
                    
                    if backtrack(vehicle_index + 1):
                        return True
                    
                    # Backtrack
                    used_indices.remove(i)
                    used_listings.pop()
            
            return False
        
        if backtrack(0):
            return used_listings
        else:
            return []
    
    @staticmethod
    def calculate_total_price(listings: List[Listing]) -> int:
        """
        Calculate total price for a list of listings
        
        Args:
            listings: List of listings
            
        Returns:
            int: Total price in cents
        """
        return sum(listing.price_in_cents for listing in listings)