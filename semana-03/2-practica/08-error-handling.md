# Practice 8: Basic Error Handling

## Objective

Learn basic error handling in FastAPI.

## Time: 60 minutes

## Implementation

### Step 1: Using HTTPException (30 min)

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 1 or user_id > len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id - 1]
```

### Step 2: Add Error Handling to All Endpoints (30 min)

Add proper error responses to your GET, POST, PUT, and DELETE endpoints.

## Deliverable

All endpoints return proper error messages when something goes wrong.
