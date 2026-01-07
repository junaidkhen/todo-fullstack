from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from src.auth.jwt import get_current_user
import os
import jwt
from datetime import datetime, timedelta

router = APIRouter()

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user_id: str
    email: str
    token: str
    message: str

# Secret key for JWT generation (should match the one used for validation)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "default-secret-key-change-in-production")
ALGORITHM = "HS256"

@router.post("/signup")
async def signup(auth_request: AuthRequest):
    """
    Signup endpoint - creates a new user and returns a JWT token.
    In a real implementation, this would interact with a user database.
    For this implementation, we'll simulate the process.
    """
    # In a real implementation, we would:
    # 1. Validate the email format
    # 2. Check if user already exists
    # 3. Hash the password
    # 4. Create user in database
    # 5. Generate JWT token

    # For simulation purposes, we'll just create a mock user
    user_id = f"user_{auth_request.email.split('@')[0]}_{int(datetime.utcnow().timestamp())}"

    # Create JWT token
    token_data = {
        "sub": user_id,  # Subject (user ID)
        "email": auth_request.email,
        "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        "iat": datetime.utcnow(),  # Issued at
    }

    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "user_id": user_id,
        "email": auth_request.email,
        "token": token,
        "message": "Account created successfully"
    }

@router.post("/signin")
async def signin(auth_request: AuthRequest):
    """
    Signin endpoint - authenticates user and returns a JWT token.
    In a real implementation, this would validate credentials against a database.
    For this implementation, we'll simulate the process.
    """
    # In a real implementation, we would:
    # 1. Look up user by email
    # 2. Verify password hash
    # 3. Generate JWT token

    # For simulation purposes, we'll just validate basic format and create a token
    if len(auth_request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    user_id = f"user_{auth_request.email.split('@')[0]}_{int(datetime.utcnow().timestamp())}"

    # Create JWT token
    token_data = {
        "sub": user_id,  # Subject (user ID)
        "email": auth_request.email,
        "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        "iat": datetime.utcnow(),  # Issued at
    }

    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "user_id": user_id,
        "email": auth_request.email,
        "token": token,
        "message": "Signed in successfully"
    }

@router.post("/signout")
async def signout():
    """
    Signout endpoint - in a real implementation, this might invalidate tokens.
    """
    return {"message": "Signed out successfully"}

@router.get("/session")
async def get_session(current_user_id: str = Depends(get_current_user)):
    """
    Get current session information using JWT validation.
    """
    return {
        "user_id": current_user_id,
        "message": "Valid session"
    }