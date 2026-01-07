from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Optional
import os

# Get the auth secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "default-secret-key-change-in-production")
ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get current user from JWT token.

    Extracts user_id from the JWT token that comes from Better Auth.
    """
    token = credentials.credentials

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user_id from the 'sub' claim (subject - typically the user ID)
        user_id: str = payload.get("sub")

        # Also check for 'id' field which might be used by Better Auth
        if user_id is None:
            user_id = payload.get("id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user ID found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials - {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )