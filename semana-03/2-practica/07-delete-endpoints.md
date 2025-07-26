# Practice 7: DELETE Endpoints

## Objective

Learn to create DELETE endpoints to remove data from your API.

## Time: 60 minutes

## Implementation

### Step 1: Basic DELETE Endpoint (30 min)

Create a simple DELETE endpoint:

```python
# In your main.py
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            deleted_user = users.pop(i)
            return {"message": f"User {deleted_user['name']} deleted"}
    return {"error": "User not found"}
```

### Step 2: Test Your Endpoint (30 min)

Test with different scenarios:

- Delete existing user
- Try to delete non-existent user

## Deliverable

Working DELETE endpoint that removes users from the list.
