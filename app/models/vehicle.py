"""
Vehicle model definition
"""

from pydantic import BaseModel, Field
from typing import List


class Vehicle(BaseModel):
    """
    Represents a vehicle with its dimensions and quantity
    """
    length: int = Field(..., ge=1, le=100, description="Length of the vehicle in feet")
    quantity: int = Field(..., ge=1, le=5, description="Number of vehicles of this type")
    
    @property
    def width(self) -> int:
        """Fixed width for all vehicles as per requirements"""
        return 10
    
    @property
    def area(self) -> int:
        """Calculate the area of the vehicle"""
        return self.length * self.width
    
    def to_individual_vehicles(self) -> List['VehicleUnit']:
        """Convert to individual vehicle units"""
        from .vehicle_unit import VehicleUnit
        return [
            VehicleUnit(length=self.length, width=self.width)
            for _ in range(self.quantity)
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "length": 20,
                "quantity": 2
            }
        }