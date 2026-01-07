"""
Pytest configuration and shared fixtures for testing.
"""
import asyncio
import pytest
import os
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import jwt
from datetime import datetime, timedelta

# Set test environment
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-testing-only"

from main import app
from src.database import get_session

# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async with async_session() as session:
        yield session

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Create an HTTP client for testing with database session override."""

    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_token() -> str:
    """Generate a test JWT token for a test user."""
    secret = os.getenv("BETTER_AUTH_SECRET")
    payload = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow().timestamp()
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def test_user_token_2() -> str:
    """Generate a second test JWT token for multi-user tests."""
    secret = os.getenv("BETTER_AUTH_SECRET")
    payload = {
        "sub": "test_user_456",
        "email": "test2@example.com",
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow().timestamp()
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def expired_token() -> str:
    """Generate an expired JWT token for testing auth failures."""
    secret = os.getenv("BETTER_AUTH_SECRET")
    payload = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "exp": datetime.utcnow() - timedelta(days=1),  # Expired
        "iat": datetime.utcnow().timestamp()
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def invalid_token() -> str:
    """Generate an invalid JWT token for testing auth failures."""
    return "invalid.token.string"


@pytest.fixture
def auth_headers(test_user_token):
    """Generate auth headers with valid token."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def auth_headers_2(test_user_token_2):
    """Generate auth headers for second user."""
    return {"Authorization": f"Bearer {test_user_token_2}"}
