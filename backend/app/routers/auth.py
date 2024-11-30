import json
from datetime import timedelta
from typing import Any, Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from ..schemas.auth.routes.login import LoginInput, LoginResponse
from ..schemas.auth.routes.logout import LogoutResponse
from ..schemas.auth.routes.me import MeResponse
from ..schemas.auth.routes.register import RegisterInput, RegisterResponse
from ..utils.auth import (
    create_access_token,
    get_admin_token,
    get_authentik_tokens,
    get_current_user_from_token,
)
from ..utils.config import settings
from ..utils.logger import get_logger

router = APIRouter(tags=["Auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

logger = get_logger(__name__)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Registers a new user in Authentik.",
    response_description="Successfully registered user",
    responses={
        201: {
            "content": {"application/json": {"example": {"message": " ✅ User registered successfully"}}},
        },
        400: {
            "description": "Invalid input",
            "content": {"application/json": {"example": {"detail": " ❌ Registration failed: Invalid input"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": " ❌ Registration error: Internal server error"}}},
        },
    },
)
async def register(user_data: RegisterInput) -> RegisterResponse:
    """
    Registers a new user in Authentik.

    This endpoint accepts user registration data and creates a new user account
    in the Authentik authentication system using an API token.

    :param RegisterInput user_data: The user registration information
    :return RegisterResponse: Success message
    :raises HTTPException:
        - 400 Bad Request: If registration data is invalid
        - 500 Internal Server Error: If there's an unexpected error during registration
    """
    try:
        access_token, token_type = await get_admin_token()
        print(access_token, token_type)
        async with httpx.AsyncClient() as client:
            request_data = user_data.model_dump(mode="json")
            response = await client.post(
                f"{settings.AUTHENTIK_URL}/api/v3/core/users/",
                json=request_data,
                headers={
                    "Authorization": f"{token_type} {access_token}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 201:
                logger.error(f" ⚠️ Registration failed with response: {response.text}")

            if response.status_code == 201:
                logger.info(" ✅ User registered successfully")
                return RegisterResponse(message=" ✅ User registered successfully")

            error_detail = response.text
            try:
                error_json = response.json()
                if isinstance(error_json, dict):
                    error_detail = error_json.get("detail", error_json)
            except json.JSONDecodeError:
                logger.error(" ❌ Failed to parse error response as JSON")
            except Exception as e:
                logger.error(f" ❌ Error processing response: {str(e)}")

            raise HTTPException(status_code=response.status_code, detail=f" ❌ Registration failed: {error_detail}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f" ❌ Unexpected registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Registration error: {str(e)}"
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticates a user against Authentik and returns access tokens.",
    response_description="Successfully authenticated user",
    responses={
        200: {
            "content": {
                "application/json": {"example": {"access_token": "token", "token_type": "bearer", "expires_in": 1800}}
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {"application/json": {"example": {"detail": " ❌ Invalid credentials"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": " ❌ Login failed: Internal server error"}}},
        },
    },
)
async def login(response: Response, user_data: LoginInput) -> LoginResponse:
    """
    Authenticates a user against Authentik and returns access tokens.

    :param Response response: FastAPI response object for setting cookies
    :param LoginInput user_data: The user credentials for authentication
    :return LoginResponse: Access token and related information
    :raises HTTPException: If authentication fails
    """
    try:
        # Get tokens from Authentik
        auth_result = await get_authentik_tokens(user_data.username, user_data.password, user_data.mfa_code)

        # Create our own access token that includes user info
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user_data.username,
                "authentik_token": auth_result["access_token"],
                "scope": auth_result.get("scope", ""),
            },
            expires_delta=access_token_expires,
        )

        # Set secure cookie with access token
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,  # Prevents JavaScript access
            secure=True,  # Only sent over HTTPS
            samesite="lax",  # Protects against CSRF
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",  # Available across all paths
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" ❌ Login failed: {str(e)}")


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logs out the current user by clearing their access token cookie.",
    response_description="Successfully logged out user",
    responses={
        200: {
            "content": {"application/json": {"example": {"message": " ✅ Logged out successfully"}}},
        },
    },
)
async def logout(response: Response) -> LogoutResponse:
    """
    Logs out the current user.

    This endpoint clears the user's access token cookie, effectively logging them out.

    :param Response response: FastAPI response object for clearing cookies
    :return LogoutResponse: Success message
    """
    response.delete_cookie("access_token")
    return LogoutResponse(message=" ✅ Logged out successfully")


@router.get(
    "/me",
    response_model=MeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Retrieves information about the currently authenticated user.",
    response_description="Successfully retrieved user information",
    responses={
        200: {
            "content": {"application/json": {"example": {"user": {"sub": "username", "email": "user@example.com"}}}},
        },
        401: {
            "description": "Not authenticated",
            "content": {"application/json": {"example": {"detail": " ❌ Not authenticated"}}},
        },
    },
)
async def get_current_user(user: Dict[str, Any] = Depends(get_current_user_from_token)) -> MeResponse:
    """
    Retrieves information about the currently authenticated user.

    This endpoint extracts user information from the access token
    in the request cookies.

    :param Request request: FastAPI request object containing cookies
    :return MeResponse: Current user information
    :raises HTTPException:
        - 401 Unauthorized: If user is not authenticated or token is invalid
    """
    return MeResponse(user=user)
