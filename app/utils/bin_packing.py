"""
Bin packing algorithm utilities
"""

from typing import List, Set, Tuple, Optional
from math import ceil
from ..models.listing import Listing
from ..models.vehicle_unit import VehicleUnit


def _round_up_to_10(value: int) -> int:
    return int(ceil(value / 10) * 10)


class BinPackingAlgorithm:
    """
    Implements bin packing algorithm for vehicle storage optimization
    """
    
    @staticmethod
    def _fits(vehicle: VehicleUnit, listing: Listing) -> bool:
        # Listings are multiples of 10; round vehicle dims up to nearest 10
        v_len = _round_up_to_10(vehicle.length)
        v_wid = _round_up_to_10(vehicle.width)
        return (v_len <= listing.length and v_wid <= listing.width)
    
    @staticmethod
    def can_fit_vehicles(vehicles: List[VehicleUnit], listings: List[Listing]) -> bool:
        if not vehicles or not listings:
            return False
        
        sorted_vehicles = sorted(vehicles, key=lambda x: x.area, reverse=True)
        available_listings = sorted(listings, key=lambda x: x.area)
        used_listings = set()
        
        for vehicle in sorted_vehicles:
            fitted = False
            for i, listing in enumerate(available_listings):
                if i in used_listings:
                    continue
                if BinPackingAlgorithm._fits(vehicle, listing):
                    used_listings.add(i)
                    fitted = True
                    break
            if not fitted:
                return False
        return True
    
    @staticmethod
    def find_optimal_combination(vehicles: List[VehicleUnit], 
                               listings: List[Listing]) -> List[Listing]:
        if not vehicles or not listings:
            return []
        
        sorted_vehicles = sorted(vehicles, key=lambda x: x.area, reverse=True)
        sorted_listings = sorted(listings, key=lambda x: x.price_per_unit_area)
        used_listings = []
        used_indices = set()
        
        def backtrack(idx: int) -> bool:
            if idx >= len(sorted_vehicles):
                return True
            v = sorted_vehicles[idx]
            for i, l in enumerate(sorted_listings):
                if i in used_indices:
                    continue
                if BinPackingAlgorithm._fits(v, l):
                    used_indices.add(i)
                    used_listings.append(l)
                    if backtrack(idx + 1):
                        return True
                    used_indices.remove(i)
                    used_listings.pop()
            return False
        
        if backtrack(0):
            return used_listings
        return []
    
    @staticmethod
    def calculate_total_price(listings: List[Listing]) -> int:
        return sum(listing.price_in_cents for listing in listings)