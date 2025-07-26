# Practice 14: Security Basics & API Keys

## Objective

Learn fundamental security concepts and implement simple API key authentication.

## Time: 75 minutes

## Implementation

### Step 1: Security Concepts (30 min)

#### Authentication vs Authorization

- **Authentication**: "Who are you?" (verifying identity)
- **Authorization**: "What can you do?" (checking permissions)

#### API Key Basics

Simple method to identify API users.

### Step 2: Simple API Key Implementation (45 min)

```python
from fastapi import FastAPI, HTTPException, Header
from typing import Optional

app = FastAPI()

# Simple API key storage (in-memory)
VALID_API_KEYS = {
    "user123": {"name": "Alice", "role": "user"},
    "admin456": {"name": "Bob", "role": "admin"}
}

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return VALID_API_KEYS[x_api_key]

# Public endpoint (no protection)
@app.get("/")
def public_endpoint():
    return {"message": "This is a public endpoint"}

# Protected endpoint
@app.get("/protected")
def protected_endpoint(user=Depends(verify_api_key)):
    return {"message": f"Hello {user['name']}, you are authenticated!"}
```

### Step 3: Testing (15 min)

Test with headers:

```
X-API-Key: user123
```

## Deliverable

Working API with public and protected endpoints using API keys.
