"""
Search result model definition
"""

from pydantic import BaseModel, Field
from typing import List


class SearchResult(BaseModel):
    """
    Represents a search result for a location
    """
    location_id: str = Field(..., description="Identifier of the location")
    listing_ids: List[str] = Field(..., description="List of listing IDs used")
    total_price_in_cents: int = Field(..., description="Total price in cents")
    
    @property
    def total_price_dollars(self) -> float:
        """Convert total price to dollars"""
        return self.total_price_in_cents / 100
    
    class Config:
        json_schema_extra = {
            "example": {
                "location_id": "abc123",
                "listing_ids": ["def456", "ghi789"],
                "total_price_in_cents": 3000
            }
        }