"""
Main FastAPI application
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from .models import Vehicle, SearchResult
from .controllers import SearchController
from .config.settings import settings


# Global controller instance
search_controller = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    """
    # Startup
    global search_controller
    search_controller = SearchController()
    yield
    # Shutdown
    search_controller = None


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A search algorithm that allows renters to find storage locations for multiple vehicles",
    version=settings.app_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "message": settings.app_name,
        "status": "running",
        "version": settings.app_version,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
async def detailed_health_check():
    """
    Detailed health check endpoint
    """
    try:
        # Test listing service
        listing_service = search_controller.listing_service if search_controller else None
        if listing_service:
            listings = listing_service.get_all_listings()
            listing_count = len(listings)
        else:
            listing_count = 0
        
        return {
            "status": "healthy",
            "version": settings.app_version,
            "timestamp": datetime.now().isoformat(),
            "services": {
                "listing_service": "healthy" if listing_count > 0 else "unhealthy",
                "search_service": "healthy" if search_controller else "unhealthy"
            },
            "metrics": {
                "total_listings": listing_count,
                "max_vehicles_per_request": settings.max_vehicles_per_request
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.post("/search", response_model=List[SearchResult], tags=["Search"])
async def search_vehicles(vehicles: List[Vehicle]):
    """
    Search for storage locations that can accommodate the given vehicles
    
    - **vehicles**: List of vehicles with length and quantity
    - Returns all possible locations with optimal pricing
    - Results are sorted by total price in ascending order
    """
    if not search_controller:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search service not available"
        )
    
    return await search_controller.search_vehicles(vehicles)


@app.get("/stats", tags=["Statistics"])
async def get_statistics():
    """
    Get application statistics
    """
    try:
        listing_service = search_controller.listing_service if search_controller else None
        if not listing_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not available"
            )
        
        listings = listing_service.get_all_listings()
        location_groups = listing_service.get_listings_by_location()
        
        # Calculate statistics
        total_listings = len(listings)
        total_locations = len(location_groups)
        
        # Price statistics
        prices = [listing.price_in_cents for listing in listings]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        avg_price = sum(prices) / len(prices) if prices else 0
        
        # Size statistics
        areas = [listing.area for listing in listings]
        min_area = min(areas) if areas else 0
        max_area = max(areas) if areas else 0
        avg_area = sum(areas) / len(areas) if areas else 0
        
        return {
            "total_listings": total_listings,
            "total_locations": total_locations,
            "price_statistics": {
                "min_price_cents": min_price,
                "max_price_cents": max_price,
                "avg_price_cents": round(avg_price, 2),
                "min_price_dollars": round(min_price / 100, 2),
                "max_price_dollars": round(max_price / 100, 2),
                "avg_price_dollars": round(avg_price / 100, 2)
            },
            "size_statistics": {
                "min_area": min_area,
                "max_area": max_area,
                "avg_area": round(avg_area, 2)
            },
            "configuration": {
                "max_vehicles_per_request": settings.max_vehicles_per_request,
                "vehicle_width": settings.vehicle_width,
                "max_response_time_ms": settings.max_response_time_ms
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting statistics: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )