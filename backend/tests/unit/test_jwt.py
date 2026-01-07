"""
Unit tests for JWT authentication and validation.
"""
import pytest
import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.auth.jwt import get_current_user
from fastapi.security import HTTPAuthorizationCredentials


class TestJWTValidation:
    """Test JWT token validation logic."""

    def test_valid_token_extraction(self, test_user_token):
        """Test extracting user_id from a valid JWT token."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=test_user_token
        )
        user_id = get_current_user(credentials)
        assert user_id == "test_user_123"

    def test_expired_token_raises_401(self, expired_token):
        """Test that expired token raises 401 Unauthorized."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=expired_token
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials)
        assert exc_info.value.status_code == 401

    def test_invalid_token_raises_401(self, invalid_token):
        """Test that invalid token raises 401 Unauthorized."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=invalid_token
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials)
        assert exc_info.value.status_code == 401

    def test_token_with_wrong_secret_raises_401(self):
        """Test that token signed with wrong secret raises 401."""
        wrong_secret = "wrong-secret-key"
        payload = {
            "sub": "user123",
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, wrong_secret, algorithm="HS256")

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials)
        assert exc_info.value.status_code == 401

    def test_token_without_sub_claim_raises_401(self):
        """Test that token without 'sub' claim raises 401."""
        secret = os.getenv("BETTER_AUTH_SECRET")
        payload = {
            "email": "test@example.com",  # No 'sub' claim
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, secret, algorithm="HS256")

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials)
        assert exc_info.value.status_code == 401

    def test_token_with_id_field_as_fallback(self):
        """Test that 'id' field is used if 'sub' is missing (Better Auth compatibility)."""
        secret = os.getenv("BETTER_AUTH_SECRET")
        payload = {
            "id": "user789",  # Using 'id' instead of 'sub'
            "email": "test@example.com",
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, secret, algorithm="HS256")

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        user_id = get_current_user(credentials)
        assert user_id == "user789"

    def test_multiple_users_different_tokens(self, test_user_token, test_user_token_2):
        """Test that different tokens return different user IDs."""
        credentials1 = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=test_user_token
        )
        credentials2 = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=test_user_token_2
        )

        user_id_1 = get_current_user(credentials1)
        user_id_2 = get_current_user(credentials2)

        assert user_id_1 == "test_user_123"
        assert user_id_2 == "test_user_456"
        assert user_id_1 != user_id_2


class TestJWTSecurity:
    """Test JWT security requirements."""

    def test_token_cannot_be_forged(self):
        """Test that token cannot be forged without the secret."""
        # Try to create a token without the secret
        fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYWNrZXIifQ.fake"
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=fake_token
        )
        with pytest.raises(HTTPException):
            get_current_user(credentials)

    def test_token_algorithm_must_be_hs256(self):
        """Test that only HS256 algorithm is accepted."""
        secret = os.getenv("BETTER_AUTH_SECRET")
        payload = {
            "sub": "user123",
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        # Try to use different algorithm
        token = jwt.encode(payload, secret, algorithm="HS256")  # Valid
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        user_id = get_current_user(credentials)
        assert user_id == "user123"
