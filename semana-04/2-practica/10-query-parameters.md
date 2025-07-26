# Practice 10: Query Parameters Basics

## Objective

Learn to use query parameters for filtering and customizing API responses.

## Time: 75 minutes

## Implementation

### Step 1: Basic Query Parameters (35 min)

Add query parameters to filter users:

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

users = [
    {"id": 1, "name": "Alice", "age": 25, "city": "New York"},
    {"id": 2, "name": "Bob", "age": 30, "city": "London"},
    {"id": 3, "name": "Charlie", "age": 35, "city": "Paris"}
]

@app.get("/users")
def get_users(
    city: Optional[str] = None,
    min_age: Optional[int] = None
):
    filtered_users = users

    if city:
        filtered_users = [u for u in filtered_users if u["city"].lower() == city.lower()]

    if min_age:
        filtered_users = [u for u in filtered_users if u["age"] >= min_age]

    return {"users": filtered_users, "count": len(filtered_users)}
```

### Step 2: Query Parameters with Validation (40 min)

Add validation and defaults:

```python
@app.get("/users/search")
def search_users(
    name: Optional[str] = Query(None, min_length=2, max_length=50),
    age_min: int = Query(0, ge=0, le=100),
    age_max: int = Query(100, ge=0, le=100),
    limit: int = Query(10, ge=1, le=100)
):
    filtered_users = users

    if name:
        filtered_users = [u for u in filtered_users
                         if name.lower() in u["name"].lower()]

    filtered_users = [u for u in filtered_users
                     if age_min <= u["age"] <= age_max]

    return {
        "users": filtered_users[:limit],
        "total": len(filtered_users),
        "filters": {
            "name": name,
            "age_range": f"{age_min}-{age_max}",
            "limit": limit
        }
    }
```

## Test Examples

- `GET /users?city=London`
- `GET /users?min_age=30`
- `GET /users/search?name=a&age_min=20&limit=5`

## Deliverable

Working API with query parameter filtering.
