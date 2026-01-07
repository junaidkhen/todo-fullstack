# Database Modeling with SQLModel & PostgreSQL

## Overview
Designing and implementing database schemas using SQLModel (combining SQLAlchemy and Pydantic) with PostgreSQL for type-safe, async database operations.

## Key Features
- **Type Safety**: Python type hints for database models
- **Pydantic Integration**: Automatic validation and serialization
- **Async Support**: Non-blocking database operations with asyncpg
- **Migration Support**: Schema versioning with Alembic
- **ORM Capabilities**: Relationships, queries, and transactions

## Application in This Project
- Neon PostgreSQL (serverless) as database
- SQLModel for data models and ORM
- Async database driver (asyncpg)
- User and Task models with relationships
- Database connection pooling

## Example Models
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

## Best Practices
- Define clear relationships between models
- Use proper field types and constraints
- Implement indexes for frequently queried fields
- Use async sessions for database operations
- Handle transactions properly
- Implement proper error handling
- Use migrations for schema changes
