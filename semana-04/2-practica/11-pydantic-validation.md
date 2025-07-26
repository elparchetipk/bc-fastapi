# Practice 11: Pydantic Field Validation

## Objective

Learn advanced data validation using Pydantic Field constraints.

## Time: 75 minutes

## Implementation

### Step 1: Field Validation Basics (35 min)

Update your user model with Field validation:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="User's full name")
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$', description="Valid email address")
    age: int = Field(..., ge=0, le=120, description="User's age")
    city: str = Field(..., min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500, description="User biography")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    age: Optional[int] = Field(None, ge=0, le=120)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
```

### Step 2: Custom Validation (40 min)

Add custom validators:

```python
from pydantic import validator

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    age: int = Field(..., ge=0, le=120)
    city: str = Field(..., min_length=2, max_length=100)

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('Name must contain at least one space')
        return v.title()

    @validator('city')
    def city_must_be_valid(cls, v):
        valid_cities = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']
        if v not in valid_cities:
            raise ValueError(f'City must be one of: {", ".join(valid_cities)}')
        return v

# Update your endpoints to use the new models
@app.post("/users")
def create_user(user: User):
    new_id = max([u["id"] for u in users], default=0) + 1
    new_user = {"id": new_id, **user.dict()}
    users.append(new_user)
    return new_user

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    for i, existing_user in enumerate(users):
        if existing_user["id"] == user_id:
            update_data = user_update.dict(exclude_unset=True)
            users[i].update(update_data)
            return users[i]
    raise HTTPException(status_code=404, detail="User not found")
```

## Test Cases

Try these to see validation in action:

- Invalid email format
- Name without space
- Age outside range (negative or >120)
- Invalid city name

## Deliverable

API with comprehensive Field validation and custom validators.
