# Practice 16: Basic Endpoint Protection

## Objective

Learn to protect endpoints with simple authentication checks.

## Time: 90 minutes

## Implementation

### Step 1: Username-Based Protection (45 min)

```python
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional

# Simple session storage (in-memory)
active_sessions = {}

def get_current_user(username: Optional[str] = None):
    if not username:
        raise HTTPException(status_code=401, detail="Username required")

    if username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    return users_db[username]

def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# User-only endpoint
@app.get("/profile")
def get_profile(user=Depends(get_current_user)):
    return {"profile": user["username"], "email": user["email"]}

# Admin-only endpoint
@app.get("/admin/users")
def list_all_users(admin=Depends(require_admin)):
    return {"users": list(users_db.keys()), "requested_by": admin["username"]}

# User-specific data
@app.get("/tasks")
def get_user_tasks(user=Depends(get_current_user)):
    # Simulate user-specific data
    return {"tasks": [f"Task 1 for {user['username']}", f"Task 2 for {user['username']}"]}
```

### Step 2: Resource Ownership (30 min)

```python
# Tasks storage per user
user_tasks = {
    "alice": [{"id": 1, "title": "Alice's task 1"}, {"id": 2, "title": "Alice's task 2"}],
    "bob": [{"id": 3, "title": "Bob's task 1"}]
}

@app.get("/my-tasks")
def get_my_tasks(user=Depends(get_current_user)):
    username = user["username"]
    return {"tasks": user_tasks.get(username, [])}

@app.post("/my-tasks")
def create_task(task_title: str, user=Depends(get_current_user)):
    username = user["username"]
    if username not in user_tasks:
        user_tasks[username] = []

    new_task = {"id": len(user_tasks[username]) + 1, "title": task_title}
    user_tasks[username].append(new_task)

    return {"message": "Task created", "task": new_task}
```

### Step 3: Testing Protection (15 min)

Test different scenarios:

- Access without authentication
- User accessing admin endpoints
- Admin accessing user data

## Deliverable

Protected endpoints with role-based access control.
