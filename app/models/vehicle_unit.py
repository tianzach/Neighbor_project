"""
Individual vehicle unit model
"""

from pydantic import BaseModel, Field


class VehicleUnit(BaseModel):
    """
    Represents an individual vehicle unit with dimensions
    """
    length: int = Field(..., description="Length of the vehicle in feet")
    width: int = Field(..., description="Width of the vehicle in feet")
    
    @property
    def area(self) -> int:
        """Calculate the area of the vehicle unit"""
        return self.length * self.width
    
    def fits_in(self, listing) -> bool:
        """
        Check if this vehicle unit fits in the given listing
        """
        return (self.length <= listing.length and 
                self.width <= listing.width)