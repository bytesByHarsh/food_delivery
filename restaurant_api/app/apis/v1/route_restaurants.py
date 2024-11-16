# Built-in Dependencies
from typing import Annotated, Dict
from datetime import timedelta
from uuid import UUID

# Third-party Dependencies
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from fastapi import Response, Request, Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.schemas.v1.schema_restaurant import RestaurantReadOpen
from app.utils.paginated import PaginatedListResponse
from app.db.session import async_get_db

from app.db.crud.crud_restaurant import get_restaurant_byID, get_restaurant_list
from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)

router = APIRouter(tags=["Restaurant Management"])

@router.get("/info/{restaurant_id}", response_model=RestaurantReadOpen)
async def get_restaurant_info(
    request: Request,
    restaurant_id: UUID,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    restaurant =  await get_restaurant_byID(
        db=db,
        id=restaurant_id
    )
    if restaurant is None:
        raise NotFoundException(f"No Restaurant with id:{restaurant_id}")
    return restaurant

@router.get("/list", response_model=PaginatedListResponse[RestaurantReadOpen])
async def restaurant_list(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    return await get_restaurant_list(
        db=db,
        page=page,
        items_per_page=items_per_page
    )