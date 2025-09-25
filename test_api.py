"""
Test script for the Multi-Vehicle Search API
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    print("✅ Health check passed")

def test_single_vehicle_search():
    """Test searching for a single vehicle"""
    print("Testing single vehicle search...")
    
    payload = [
        {
            "length": 10,
            "quantity": 1
        }
    ]
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/search", json=payload)
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that we got results
    assert len(data) > 0
    
    # Check that results are sorted by price
    prices = [result["total_price_in_cents"] for result in data]
    assert prices == sorted(prices)
    
    # Check that response time is reasonable
    response_time = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"Response time: {response_time:.2f}ms")
    assert response_time < 300  # Should be under 300ms
    
    print(f"✅ Single vehicle search passed - found {len(data)} locations")

def test_multiple_vehicles_search():
    """Test searching for multiple vehicles"""
    print("Testing multiple vehicles search...")
    
    payload = [
        {
            "length": 10,
            "quantity": 1
        },
        {
            "length": 20,
            "quantity": 2
        }
    ]
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/search", json=payload)
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that we got results
    assert len(data) > 0
    
    # Check that each result has the correct number of listings
    for result in data:
        total_vehicles = sum(vehicle["quantity"] for vehicle in payload)
        assert len(result["listing_ids"]) == total_vehicles
    
    # Check that results are sorted by price
    prices = [result["total_price_in_cents"] for result in data]
    assert prices == sorted(prices)
    
    response_time = (end_time - start_time) * 1000
    print(f"Response time: {response_time:.2f}ms")
    assert response_time < 300
    
    print(f"✅ Multiple vehicles search passed - found {len(data)} locations")

def test_invalid_input():
    """Test invalid input handling"""
    print("Testing invalid input...")
    
    # Test too many vehicles
    payload = [
        {"length": 10, "quantity": 6}  # More than 5 total vehicles
    ]
    
    response = requests.post(f"{BASE_URL}/search", json=payload)
    assert response.status_code == 400
    
    # Test zero vehicles
    payload = []
    response = requests.post(f"{BASE_URL}/search", json=payload)
    assert response.status_code == 400
    
    print("✅ Invalid input handling passed")

def test_example_from_readme():
    """Test the example from the README"""
    print("Testing README example...")
    
    payload = [
        {
            "length": 10,
            "quantity": 1
        },
        {
            "length": 20,
            "quantity": 2
        },
        {
            "length": 25,
            "quantity": 1
        }
    ]
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/search", json=payload)
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that we got results
    assert len(data) > 0
    
    # Check that each result has the correct number of listings (4 total vehicles)
    for result in data:
        assert len(result["listing_ids"]) == 4
    
    # Check that results are sorted by price
    prices = [result["total_price_in_cents"] for result in data]
    assert prices == sorted(prices)
    
    response_time = (end_time - start_time) * 1000
    print(f"Response time: {response_time:.2f}ms")
    assert response_time < 300
    
    print(f"✅ README example passed - found {len(data)} locations")
    
    # Print first few results for verification
    print("\nFirst 3 results:")
    for i, result in enumerate(data[:3]):
        print(f"  {i+1}. Location: {result['location_id'][:8]}... Price: ${result['total_price_in_cents']/100:.2f}")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting API tests...\n")
    
    try:
        test_health_check()
        print()
        
        test_single_vehicle_search()
        print()
        
        test_multiple_vehicles_search()
        print()
        
        test_invalid_input()
        print()
        
        test_example_from_readme()
        print()
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    run_all_tests()