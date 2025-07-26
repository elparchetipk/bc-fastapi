# Practice 12: Search Endpoints

## Objective

Create powerful search endpoints with multiple filtering options.

## Time: 90 minutes

## Implementation

### Step 1: Text Search (45 min)

Create a search endpoint that can search across multiple fields:

```python
from fastapi import FastAPI, Query
from typing import Optional, List

@app.get("/users/search")
def search_users(
    q: Optional[str] = Query(None, min_length=1, description="Search query"),
    city: Optional[str] = Query(None, description="Filter by city"),
    min_age: Optional[int] = Query(None, ge=0, description="Minimum age"),
    max_age: Optional[int] = Query(None, le=120, description="Maximum age"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Skip results")
):
    filtered_users = users.copy()

    # Text search across name and bio
    if q:
        filtered_users = [
            user for user in filtered_users
            if (q.lower() in user["name"].lower() or
                (user.get("bio") and q.lower() in user["bio"].lower()))
        ]

    # Filter by city
    if city:
        filtered_users = [
            user for user in filtered_users
            if user["city"].lower() == city.lower()
        ]

    # Filter by age range
    if min_age is not None:
        filtered_users = [
            user for user in filtered_users
            if user["age"] >= min_age
        ]

    if max_age is not None:
        filtered_users = [
            user for user in filtered_users
            if user["age"] <= max_age
        ]

    # Apply pagination
    total = len(filtered_users)
    paginated_users = filtered_users[offset:offset + limit]

    return {
        "users": paginated_users,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + limit < total
    }
```

### Step 2: Advanced Sorting (45 min)

Add sorting capabilities:

```python
@app.get("/users/advanced-search")
def advanced_search(
    q: Optional[str] = Query(None, min_length=1),
    city: Optional[str] = None,
    min_age: Optional[int] = Query(None, ge=0),
    max_age: Optional[int] = Query(None, le=120),
    sort_by: str = Query("name", regex="^(name|age|city)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    filtered_users = users.copy()

    # Apply all filters (same as before)
    if q:
        filtered_users = [
            user for user in filtered_users
            if q.lower() in user["name"].lower()
        ]

    if city:
        filtered_users = [
            user for user in filtered_users
            if user["city"].lower() == city.lower()
        ]

    if min_age is not None:
        filtered_users = [
            user for user in filtered_users
            if user["age"] >= min_age
        ]

    if max_age is not None:
        filtered_users = [
            user for user in filtered_users
            if user["age"] <= max_age
        ]

    # Apply sorting
    reverse_order = sort_order == "desc"
    filtered_users.sort(key=lambda x: x[sort_by], reverse=reverse_order)

    # Apply pagination
    total = len(filtered_users)
    paginated_users = filtered_users[offset:offset + limit]

    return {
        "users": paginated_users,
        "total": total,
        "limit": limit,
        "offset": offset,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "filters_applied": {
            "search": q,
            "city": city,
            "age_range": f"{min_age or 0}-{max_age or 120}"
        }
    }
```

## Test Examples

- `GET /users/search?q=alice`
- `GET /users/search?city=London&min_age=25&limit=5`
- `GET /users/advanced-search?sort_by=age&sort_order=desc&limit=3`

## Deliverable

Complete search API with filtering, sorting, and pagination.
