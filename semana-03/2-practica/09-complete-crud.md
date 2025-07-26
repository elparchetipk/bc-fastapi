# Practice 9: Complete CRUD API

## Objective

Consolidate all CRUD operations into a complete API.

## Time: 60 minutes

## Implementation

### Step 1: Complete API File (45 min)

Create a complete API with all operations:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simple data store
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

class User(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str = None
    email: str = None

# GET all users
@app.get("/users")
def get_users():
    return users

# GET single user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# POST new user
@app.post("/users")
def create_user(user: User):
    new_id = max([u["id"] for u in users]) + 1 if users else 1
    new_user = {"id": new_id, **user.dict()}
    users.append(new_user)
    return new_user

# PUT update user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for i, existing_user in enumerate(users):
        if existing_user["id"] == user_id:
            users[i] = {"id": user_id, **user.dict()}
            return users[i]
    raise HTTPException(status_code=404, detail="User not found")

# DELETE user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            deleted_user = users.pop(i)
            return {"message": f"User {deleted_user['name']} deleted"}
    raise HTTPException(status_code=404, detail="User not found")
```

### Step 2: Test Complete API (15 min)

Test all endpoints to ensure they work together properly.

## Deliverable

Complete working CRUD API with proper error handling.
