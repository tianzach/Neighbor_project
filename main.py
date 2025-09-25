"""
Multi-Vehicle Search API
A search algorithm for finding storage locations for multiple vehicles.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
from datetime import datetime

app = FastAPI(
    title="Multi-Vehicle Search API",
    description="Find optimal storage locations for multiple vehicles",
    version="1.0.0"
)

# Data models
class Vehicle(BaseModel):
    length: int
    quantity: int

class SearchResult(BaseModel):
    location_id: str
    listing_ids: List[str]
    total_price_in_cents: int

# Global variable to store listings data
listings_data = None

def load_listings_data():
    """Load and cache the listings data"""
    global listings_data
    if listings_data is None:
        try:
            with open('listings.json', 'r') as f:
                listings_data = json.load(f)
            print(f"Loaded {len(listings_data)} listings")
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Listings data not found")
    return listings_data

def can_fit_vehicles(vehicles: List[Vehicle], listings: List[Dict]) -> bool:
    """
    Check if a list of vehicles can fit in a list of listings using bin packing algorithm
    """
    # Create a list of all vehicles with their dimensions
    all_vehicles = []
    for vehicle in vehicles:
        for _ in range(vehicle.quantity):
            all_vehicles.append({
                'length': vehicle.length,
                'width': 10  # Fixed width as per requirements
            })
    
    # Sort vehicles by area (length * width) descending for better packing
    all_vehicles.sort(key=lambda x: x['length'] * x['width'], reverse=True)
    
    # Sort listings by area ascending to use smaller spaces first
    available_listings = sorted(listings, key=lambda x: x['length'] * x['width'])
    
    # Track which listings are used
    used_listings = set()
    
    # Try to fit each vehicle
    for vehicle in all_vehicles:
        fitted = False
        for i, listing in enumerate(available_listings):
            if i in used_listings:
                continue
            
            # Check if vehicle fits in listing
            if (vehicle['length'] <= listing['length'] and 
                vehicle['width'] <= listing['width']):
                used_listings.add(i)
                fitted = True
                break
        
        if not fitted:
            return False
    
    return True

def find_optimal_combination(vehicles: List[Vehicle], location_listings: List[Dict]) -> List[Dict]:
    """
    Find the optimal combination of listings for a location using dynamic programming approach
    """
    # Create a list of all vehicles with their dimensions
    all_vehicles = []
    for vehicle in vehicles:
        for _ in range(vehicle.quantity):
            all_vehicles.append({
                'length': vehicle.length,
                'width': 10
            })
    
    # Sort vehicles by area descending for better packing
    all_vehicles.sort(key=lambda x: x['length'] * x['width'], reverse=True)
    
    # Sort listings by price per unit area (ascending) for optimal cost
    sorted_listings = sorted(location_listings, 
                           key=lambda x: x['price_in_cents'] / (x['length'] * x['width']))
    
    # Use a greedy approach with backtracking to find optimal combination
    used_listings = []
    used_indices = set()
    
    def backtrack(vehicle_index):
        if vehicle_index >= len(all_vehicles):
            return True
        
        vehicle = all_vehicles[vehicle_index]
        
        for i, listing in enumerate(sorted_listings):
            if i in used_indices:
                continue
            
            # Check if vehicle fits in listing
            if (vehicle['length'] <= listing['length'] and 
                vehicle['width'] <= listing['width']):
                
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

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Multi-Vehicle Search API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/search", response_model=List[SearchResult])
async def search_vehicles(vehicles: List[Vehicle]):
    """
    Search for storage locations that can accommodate the given vehicles
    """
    # Validate input
    total_quantity = sum(vehicle.quantity for vehicle in vehicles)
    if total_quantity > 5:
        raise HTTPException(status_code=400, detail="Total vehicle quantity cannot exceed 5")
    
    if total_quantity == 0:
        raise HTTPException(status_code=400, detail="At least one vehicle is required")
    
    # Load listings data
    listings = load_listings_data()
    
    # Group listings by location_id
    location_groups = {}
    for listing in listings:
        location_id = listing['location_id']
        if location_id not in location_groups:
            location_groups[location_id] = []
        location_groups[location_id].append(listing)
    
    results = []
    
    # Check each location
    for location_id, location_listings in location_groups.items():
        if can_fit_vehicles(vehicles, location_listings):
            # Find optimal combination for this location
            optimal_listings = find_optimal_combination(vehicles, location_listings)
            
            if optimal_listings:
                total_price = sum(listing['price_in_cents'] for listing in optimal_listings)
                listing_ids = [listing['id'] for listing in optimal_listings]
                
                results.append(SearchResult(
                    location_id=location_id,
                    listing_ids=listing_ids,
                    total_price_in_cents=total_price
                ))
    
    # Sort by total price (ascending)
    results.sort(key=lambda x: x.total_price_in_cents)
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)