"""
Listing model definition
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class Listing(BaseModel):
    """
    Represents a storage listing
    """
    id: str = Field(..., description="Unique identifier for the listing")
    location_id: str = Field(..., description="Identifier of the location")
    length: int = Field(..., description="Length of the listing in feet")
    width: int = Field(..., description="Width of the listing in feet")
    price_in_cents: int = Field(..., description="Price in cents")
    
    @property
    def area(self) -> int:
        """Calculate the area of the listing"""
        return self.length * self.width
    
    @property
    def price_per_unit_area(self) -> float:
        """Calculate price per unit area"""
        return self.price_in_cents / self.area if self.area > 0 else 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Listing':
        """Create Listing from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.dict()
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "abc123",
                "location_id": "def456",
                "length": 20,
                "width": 10,
                "price_in_cents": 1500
            }
        }