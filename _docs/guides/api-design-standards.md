# API Design & Documentation Standards

## 🎯 RESTful API Design Principles

### HTTP Methods & Status Codes

```python
# Standard HTTP methods usage
GET    /api/users          # List all users (200)
GET    /api/users/123      # Get specific user (200, 404)
POST   /api/users          # Create new user (201, 400, 409)
PUT    /api/users/123      # Update entire user (200, 404, 400)
PATCH  /api/users/123      # Partial update (200, 404, 400)
DELETE /api/users/123      # Delete user (204, 404)
```

### Resource Naming Conventions

```python
# ✅ GOOD: Consistent, predictable patterns
/api/users                  # Collection
/api/users/123             # Resource
/api/users/123/posts       # Nested collection
/api/users/123/posts/456   # Nested resource

# ❌ BAD: Inconsistent patterns
/api/getUsers              # Verb in URL
/api/user_posts           # Inconsistent naming
/api/users/123/getPosts   # Verb in nested resource
```

## 📖 OpenAPI Documentation Standards

### Complete Endpoint Documentation

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

class UserResponse(BaseModel):
    id: int = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")
    username: str = Field(..., description="Username (3-20 characters)")
    created_at: datetime = Field(..., description="Account creation timestamp")
    is_active: bool = Field(..., description="User account status")

class UserCreateRequest(BaseModel):
    email: str = Field(..., description="Valid email address", example="user@example.com")
    username: str = Field(..., description="Username (3-20 characters)", example="john_doe")
    password: str = Field(..., description="Strong password (8+ characters)", example="SecurePass123!")

@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user account",
    description="""
    Create a new user account with email and username.

    - **email**: Must be a valid email format and unique
    - **username**: 3-20 characters, alphanumeric and underscore only
    - **password**: Minimum 8 characters with uppercase, lowercase, and number

    Returns the created user information (password excluded).
    """,
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "email": "user@example.com",
                        "username": "john_doe",
                        "created_at": "2024-01-01T12:00:00Z",
                        "is_active": True
                    }
                }
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        409: {
            "description": "Email or username already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered"
                    }
                }
            }
        }
    },
    tags=["Users"]
)
async def create_user(user_data: UserCreateRequest):
    # Implementation here
    pass
```

### Error Response Standards

```python
from enum import Enum
from typing import Optional

class ErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"

class ErrorResponse(BaseModel):
    error_code: ErrorCode
    message: str
    details: Optional[dict] = None
    timestamp: datetime
    path: str

# Standard error responses
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error_code=ErrorCode.VALIDATION_ERROR,
            message="Validation failed",
            details={"errors": exc.errors()},
            timestamp=datetime.utcnow(),
            path=str(request.url.path)
        ).dict()
    )
```

## 🔄 Versioning Strategy

### URL Versioning (Recommended)

```python
# Version in URL path
@app.get("/api/v1/users")
async def get_users_v1():
    # Version 1 implementation
    pass

@app.get("/api/v2/users")
async def get_users_v2():
    # Version 2 implementation with new features
    pass

# Gradual migration strategy
@app.get("/api/users")  # Latest version alias
async def get_users():
    return await get_users_v2()
```

### Header Versioning (Alternative)

```python
from fastapi import Header

@app.get("/api/users")
async def get_users(api_version: str = Header("v1", alias="API-Version")):
    if api_version == "v1":
        return await get_users_v1()
    elif api_version == "v2":
        return await get_users_v2()
    else:
        raise HTTPException(400, "Unsupported API version")
```

## 📊 Pagination Standards

### Cursor-based Pagination (Recommended)

```python
class PaginationParams(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="Number of items per page")
    cursor: Optional[str] = Field(None, description="Pagination cursor")

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: dict = Field(..., description="Pagination metadata")

@app.get("/api/users", response_model=PaginatedResponse[UserResponse])
async def get_users(pagination: PaginationParams = Depends()):
    users = await get_users_paginated(pagination.limit, pagination.cursor)

    return PaginatedResponse(
        data=users,
        pagination={
            "limit": pagination.limit,
            "next_cursor": users[-1].id if len(users) == pagination.limit else None,
            "has_more": len(users) == pagination.limit
        }
    )
```

### Offset-based Pagination (Simple cases)

```python
class OffsetPagination(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Items per page")

@app.get("/api/posts")
async def get_posts(pagination: OffsetPagination = Depends()):
    offset = (pagination.page - 1) * pagination.size
    posts = await get_posts_with_offset(pagination.size, offset)
    total = await count_posts()

    return {
        "data": posts,
        "pagination": {
            "page": pagination.page,
            "size": pagination.size,
            "total": total,
            "pages": math.ceil(total / pagination.size)
        }
    }
```

## 🔍 Filtering & Searching

### Query Parameter Standards

```python
from typing import Optional, List
from fastapi import Query

class UserFilters(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

@app.get("/api/users")
async def get_users(
    # Search
    search: Optional[str] = Query(None, description="Search in email and username"),

    # Filtering
    email: Optional[str] = Query(None, description="Filter by exact email"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date"),

    # Sorting
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),

    # Pagination
    pagination: PaginationParams = Depends()
):
    filters = UserFilters(
        email=email,
        is_active=is_active,
        created_after=created_after
    )

    return await get_users_filtered(filters, search, sort_by, sort_order, pagination)
```

## 🛡️ Rate Limiting Documentation

### Rate Limit Headers

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/users")
@limiter.limit("100/minute")
async def get_users(request: Request):
    """
    Get users with rate limiting.

    Rate Limits:
    - 100 requests per minute per IP
    - Headers returned:
      - X-RateLimit-Limit: Request limit per window
      - X-RateLimit-Remaining: Remaining requests in window
      - X-RateLimit-Reset: Window reset time (Unix timestamp)
    """
    pass
```

## 📋 Implementation Checklist

### API Design

- [ ] RESTful URL patterns followed
- [ ] Consistent HTTP status codes
- [ ] Proper HTTP methods usage
- [ ] Resource naming conventions
- [ ] Nested resource patterns

### Documentation

- [ ] Complete OpenAPI specification
- [ ] Request/response examples
- [ ] Error response documentation
- [ ] Authentication requirements
- [ ] Rate limiting information

### Data Validation

- [ ] Input validation with Pydantic
- [ ] Output serialization models
- [ ] Error message standardization
- [ ] Validation error formatting
- [ ] Type hints throughout

### Performance

- [ ] Pagination implemented
- [ ] Filtering capabilities
- [ ] Sorting options
- [ ] Field selection (sparse fieldsets)
- [ ] Response compression

### Security

- [ ] Authentication documented
- [ ] Authorization patterns clear
- [ ] Input sanitization
- [ ] Rate limiting configured
- [ ] CORS policy documented

## 🎯 Progressive Enhancement by Week

### Semana 2-3: Basic API Design

- RESTful endpoint patterns
- Basic CRUD operations
- HTTP status codes
- Simple validation

### Semana 4-5: Enhanced Documentation

- Complete OpenAPI specs
- Request/response examples
- Error documentation
- Authentication integration

### Semana 6-7: Advanced Features

- Pagination implementation
- Filtering and searching
- Sorting capabilities
- Validation enhancement

### Semana 8-9: Production Features

- API versioning strategy
- Rate limiting
- Advanced error handling
- Performance optimization

### Semana 10-12: Enterprise Patterns

- API testing automation
- Monitoring integration
- Documentation maintenance
- Backwards compatibility
