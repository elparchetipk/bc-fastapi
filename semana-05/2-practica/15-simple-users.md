# Practice 15: Simple User Management

## Objective

Implement basic user concepts and simple authentication patterns.

## Time: 90 minutes

## Implementation

### Step 1: User Model (30 min)

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

# In-memory user storage
users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123",  # In real apps, this would be hashed
        "role": "user"
    },
    "bob": {
        "username": "bob",
        "email": "bob@example.com",
        "password": "admin123",
        "role": "admin"
    }
}
```

### Step 2: Simple Login Logic (45 min)

```python
@app.post("/login")
def login(user_data: UserLogin):
    username = user_data.username
    password = user_data.password

    if username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid username")

    if users_db[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid password")

    # Return user info (without password)
    user_info = users_db[username].copy()
    del user_info["password"]

    return {"message": "Login successful", "user": user_info}

@app.get("/users/me")
def get_current_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_info = users_db[username].copy()
    del user_info["password"]
    return user_info
```

### Step 3: Testing Simple Authentication (15 min)

Test login with different users and verify responses.

## Deliverable

Basic user management with simple login functionality.
