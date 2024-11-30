from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

import httpx
from app.utils.config import settings
from fastapi import Cookie, Header, HTTPException, Request, status
from jose import JWTError, jwt

from .logger import get_logger

logger = get_logger(__name__)


async def get_authentik_tokens(username: str, password: str, mfa_code: str | None = None) -> Dict[str, Any]:
    """
    Authenticates user credentials against Authentik's token endpoint.

    :param str username: The username to authenticate
    :param str password: The user's password
    :param str | None mfa_code: Optional MFA code if enabled
    :return Dict[str, Any]: The token response from Authentik
    :raises HTTPException: If authentication fails
    """
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": settings.AUTHENTIK_CLIENT_ID,
        "client_secret": settings.AUTHENTIK_CLIENT_SECRET,
    }

    if mfa_code:
        data["mfa_code"] = mfa_code

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTHENTIK_URL}/application/o/token/",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                logger.info(" ✅ User authenticated successfully")
                return response.json()

            logger.error(f" ❌ Authentication failed: {response.text}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f" ❌ Authentication failed: {response.text}"
            )
        except Exception as e:
            logger.error(f" ❌ Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Authentication error: {str(e)}"
            )


def create_access_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """
    Create JWT access token

    :param Dict[str, Any] data: Data to encode in the token
    :param timedelta expires_delta: Token expiration time
    :return str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.now(datetime.UTC) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user_from_token(
    request: Request,
    authorization: str | None = Header(None),
    access_token: str | None = Cookie(None),
) -> Dict[str, Any]:
    """
    Dependency that validates the access token from either header or cookie.

    :param Request request: The FastAPI request object
    :param str | None authorization: Optional authorization header
    :param str | None access_token: Optional access token cookie
    :return Dict[str, Any]: The current user information
    :raises HTTPException: If no valid token is found
    """
    token = None

    # Check Authorization header first
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    # Then check cookie
    elif access_token and access_token.startswith("Bearer "):
        token = access_token.replace("Bearer ", "")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" ❌ Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return verify_token(token)


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.

    :param str token: The JWT token to verify
    :return Dict[str, Any]: The decoded token payload
    :raises HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" ❌ Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_admin_token() -> Tuple[str, str]:
    """
    Get an admin access token from Authentik using OAuth2 client credentials flow.
    This generates a short-lived token with specific scopes for user management.

    :return Tuple[str, str]: A tuple containing (access_token, token_type)
    :raises HTTPException: If authentication fails
    """
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.AUTHENTIK_CLIENT_ID,
        "client_secret": settings.AUTHENTIK_CLIENT_SECRET,
        "scope": "openid goauthentik.io/api goauthentik.io/api/users goauthentik.io/api/core",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTHENTIK_URL}/application/o/token/",
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
            )
            response.raise_for_status()
            result = response.json()
            return result["access_token"], result["token_type"]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Admin authentication error: {str(e)}"
            )
