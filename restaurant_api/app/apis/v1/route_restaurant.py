# Built-in Dependencies
from typing import Annotated, Dict, Any
import os

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request, File, UploadFile
import fastapi
from PIL import Image
from sqlalchemy.sql import text

# Local Dependencies
from app.core.dependencies import CurrentUser, CurrentSuperUser
from app.db.crud.crud_restaurant import create_new_restaurant, get_restaurant
from app.db.session import async_get_db
from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)
from app.schemas.v1.schema_restaurant import RestaurantCreate, RestaurantUpdate, RestaurantRead

from app.utils.paginated import (
    PaginatedListResponse,
    paginated_response,
    compute_offset,
)
from app.core.security import blacklist_token, oauth2_scheme
from app.core.config import settings

router = fastapi.APIRouter(tags=["User Management"])

@router.post("/create")
async def create_restaurant(
    request: Request,
    restaurant: RestaurantCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentSuperUser,
):
    return await create_new_restaurant(db=db, restaurant=restaurant)

@router.get("/me", response_model=RestaurantRead)
async def create_restaurant(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
):
    return current_user