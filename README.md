# Multi-Vehicle Search API

A search algorithm that allows renters to find storage locations for multiple vehicles. This API implements a variant of the bin packing problem to find optimal storage combinations.

## 🚀 Features

- **Multi-vehicle search**: Find storage for up to 5 vehicles simultaneously
- **Optimal pricing**: Returns the cheapest possible combination per location
- **Fast response**: Sub-300ms response times
- **Comprehensive results**: Returns all possible locations that can accommodate the vehicles
- **RESTful API**: Clean, well-documented endpoints

## 📋 Requirements

- Python 3.11+
- FastAPI
- Uvicorn

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Neighbor_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /
```

Returns the API status and timestamp.

**Response:**
```json
{
    "message": "Multi-Vehicle Search API",
    "status": "running",
    "timestamp": "2024-01-01T12:00:00.000000"
}
```

#### Search Vehicles
```http
POST /search
```

Searches for storage locations that can accommodate the given vehicles.

**Request Body:**
```json
[
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
```

**Response:**
```json
[
    {
        "location_id": "42b8f068-2d13-4ed1-8eec-c98f1eef0850",
        "listing_ids": ["b9bbe25f-5679-4917-bd7b-1e19c464f3a8"],
        "total_price_in_cents": 1005
    },
    {
        "location_id": "507628b8-163e-4e22-a6a3-6a16f8188928",
        "listing_ids": ["e7d59481-b804-4565-b49b-d5beb7aec350"],
        "total_price_in_cents": 1088
    }
]
```

## 🧮 Algorithm

This API implements a variant of the **bin packing problem** with the following approach:

1. **Vehicle Processing**: Convert input vehicles into individual units with dimensions (length × 10 feet width)
2. **Location Grouping**: Group all listings by location_id
3. **Feasibility Check**: For each location, check if all vehicles can fit using a bin packing algorithm
4. **Optimal Combination**: Find the cheapest combination of listings for each feasible location
5. **Result Sorting**: Sort results by total price in ascending order

### Key Features:
- **Greedy Bin Packing**: Uses a greedy approach with backtracking for optimal space utilization
- **Price Optimization**: Sorts listings by price per unit area for cost efficiency
- **Constraint Satisfaction**: Ensures all vehicles fit within the available space
- **Comprehensive Search**: Returns all possible solutions, not just the first match

## 🧪 Testing

Run the test suite:

```bash
python test_api.py
```

The test suite includes:
- Health check validation
- Single vehicle search
- Multiple vehicle search
- Invalid input handling
- README example verification
- Performance testing (response time < 300ms)

## 📊 Performance

- **Response Time**: < 300ms for typical queries
- **Data Scale**: Handles 1,000+ listings across 365+ locations
- **Memory Usage**: Efficient in-memory processing
- **Scalability**: Optimized algorithms for real-time performance

## 🚀 Deployment

### Railway Deployment (Recommended)

Railway offers free deployment without credit card requirements.

1. **Create Railway Account**
   - Visit [Railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Click "Deploy Now"

3. **Get Your URL**
   - Railway provides a public URL
   - Example: `https://your-project.railway.app`

### Heroku Deployment (Alternative)

1. Install Heroku CLI
2. Create a Heroku app:
```bash
heroku create your-app-name
```

3. Deploy:
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

4. Scale the app:
```bash
heroku ps:scale web=1
```

### Environment Variables

No environment variables are required for basic operation.

## 📝 API Usage Examples

### Example 1: Single Vehicle
```bash
# Local development
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '[{"length": 10, "quantity": 1}]'

# Railway deployment
curl -X POST "https://your-project.railway.app/search" \
  -H "Content-Type: application/json" \
  -d '[{"length": 10, "quantity": 1}]'
```

### Example 2: Multiple Vehicles
```bash
# Local development
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '[
    {"length": 10, "quantity": 1},
    {"length": 20, "quantity": 2},
    {"length": 25, "quantity": 1}
  ]'

# Railway deployment
curl -X POST "https://your-project.railway.app/search" \
  -H "Content-Type: application/json" \
  -d '[
    {"length": 10, "quantity": 1},
    {"length": 20, "quantity": 2},
    {"length": 25, "quantity": 1}
  ]'
```

## 🔧 Configuration

### Vehicle Constraints
- Maximum 5 vehicles total per request
- Vehicle width is fixed at 10 feet
- Vehicle length must be specified in feet

### Listing Data
- 1,000+ listings across 365+ locations
- Price range: $10.05 - $998.89
- 25 different size combinations
- All dimensions are multiples of 10

## 🐛 Error Handling

The API handles various error conditions:

- **400 Bad Request**: Invalid input (too many vehicles, empty request)
- **500 Internal Server Error**: Data loading issues

## 📈 Future Improvements

- [ ] Caching for improved performance
- [ ] Database integration for dynamic data
- [ ] Advanced bin packing algorithms
- [ ] Real-time availability checking
- [ ] Geographic filtering
- [ ] User authentication and preferences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of a technical assessment and is for demonstration purposes.

## 👨‍💻 Author

Developed as part of a multi-vehicle search take-home challenge.

---

**Note**: This API is designed for demonstration purposes and handles a specific dataset of 1,000 listings. In a production environment, you would want to implement proper database integration, caching, and more sophisticated algorithms.