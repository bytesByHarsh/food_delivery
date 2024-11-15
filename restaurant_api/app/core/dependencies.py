# Built-in Dependencies
from typing import Annotated, Union, Any, Dict
import logging
import os

# Third-Party Dependencies
from fastapi import Depends, HTTPException, Request
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
# from app.db.crud.crud_user import crud_users
from app.core.http_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    # RateLimitException
)

from app.db.session import async_get_db
from app.core.security import oauth2_scheme, verify_token
from app.schemas.v1.schema_restaurant import RestaurantRead

# Logger instance
logger = logging.getLogger(__name__)


async def get_current_user_base(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_get_db)
) -> RestaurantRead | None:
    user = await get_current_user(token=token, db=db)
    if user:
        return RestaurantRead(**user)
    return None


# Function to get the current user based on the provided authentication token
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_get_db)
) -> Union[Dict[str, Any], None]:
    credentials_exception = UnauthorizedException("User not authenticated.")

    token_data = await verify_token(token, db)
    if token_data is None:
        raise credentials_exception

    # Check if the authentication token represents an email or username and retrieve the user information
    if "@" in token_data.username_or_email:
        user: dict = await crud_users.get(
            db=db, email=token_data.username_or_email, is_deleted=False
        )
    else:
        user = await crud_users.get(
            db=db, username=token_data.username_or_email, is_deleted=False
        )

    if user:
        # Return the user information if available
        return user

    # Raise an exception if the user is not authenticated
    raise credentials_exception


# Function to get the optional user based on the provided request
async def get_optional_user(
    request: Request, db: AsyncSession = Depends(async_get_db)
) -> dict | None:
    token = request.headers.get("Authorization")
    if not token:
        return None

    try:
        # Parse the Authorization token and verify it to obtain token data
        token_type, _, token_value = token.partition(" ")
        if token_type.lower() != "bearer" or not token_value:
            # Return None if the token is not a bearer token
            return None

        token_data = await verify_token(token_value, db)
        if token_data is None:
            # Return None if token verification fails
            return None

        # Retrieve the current user information based on the token data
        return await get_current_user(token_value, db=db)

    except HTTPException as http_exc:
        if http_exc.status_code != 401:
            # Log unexpected HTTPException with non-401 status code.
            logger.error(
                f"Unexpected HTTPException in get_optional_user: {http_exc.detail}"
            )
        return None

    except Exception as exc:
        # Log unexpected errors during execution.
        logger.error(f"Unexpected error in get_optional_user: {exc}")
        return None


# Function to get the current superuser based on the provided current user information
async def get_current_superuser(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    if not current_user["is_superuser"]:
        raise ForbiddenException("You do not have enough privileges.")

    return current_user


def create_folders(root_folder, sub_folders):
    # Create the root folder if it doesn't exist
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    # Create sub_folders inside the root folder
    for subfolder in sub_folders:
        subfolder_path = os.path.join(root_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)


CurrentUser = Annotated[RestaurantRead, Depends(get_current_user_base)]
CurrentSuperUser = Annotated[RestaurantRead, Depends(get_current_superuser)]
