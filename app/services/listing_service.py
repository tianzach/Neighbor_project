"""
Listing service for data management
"""

import json
import os
from typing import List, Dict, Optional
from ..models.listing import Listing
from ..config.settings import settings


class ListingService:
    """
    Service for managing listing data
    """
    
    def __init__(self):
        self._listings_cache: Optional[List[Listing]] = None
        self._location_groups_cache: Optional[Dict[str, List[Listing]]] = None
    
    def load_listings(self) -> List[Listing]:
        """
        Load listings from the JSON file
        
        Returns:
            List[Listing]: List of all listings
            
        Raises:
            FileNotFoundError: If listings file is not found
            ValueError: If JSON data is invalid
        """
        if self._listings_cache is not None:
            return self._listings_cache
        
        try:
            with open(settings.listings_file_path, 'r') as f:
                data = json.load(f)
            
            listings = [Listing.from_dict(item) for item in data]
            self._listings_cache = listings
            
            print(f"Loaded {len(listings)} listings")
            return listings
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Listings file not found: {settings.listings_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in listings file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading listings: {e}")
    
    def get_listings_by_location(self) -> Dict[str, List[Listing]]:
        """
        Group listings by location_id
        
        Returns:
            Dict[str, List[Listing]]: Dictionary mapping location_id to listings
        """
        if self._location_groups_cache is not None:
            return self._location_groups_cache
        
        listings = self.load_listings()
        location_groups = {}
        
        for listing in listings:
            location_id = listing.location_id
            if location_id not in location_groups:
                location_groups[location_id] = []
            location_groups[location_id].append(listing)
        
        self._location_groups_cache = location_groups
        return location_groups
    
    def get_all_listings(self) -> List[Listing]:
        """
        Get all listings
        
        Returns:
            List[Listing]: List of all listings
        """
        return self.load_listings()
    
    def get_listings_by_location_id(self, location_id: str) -> List[Listing]:
        """
        Get listings for a specific location
        
        Args:
            location_id: The location identifier
            
        Returns:
            List[Listing]: List of listings for the location
        """
        location_groups = self.get_listings_by_location()
        return location_groups.get(location_id, [])
    
    def clear_cache(self):
        """Clear the listings cache"""
        self._listings_cache = None
        self._location_groups_cache = None