# Built-in Dependencies
from typing import Annotated, Any
from uuid import UUID
import requests

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request
import fastapi

# Local Dependencies
from app.core.dependencies import CurrentUser
from app.core.config import settings
from app.db.session import async_get_db

from app.utils.paginated import (
    PaginatedListResponse,
)

router = fastapi.APIRouter(tags=["Restaurants"])

@router.get("/list")
async def get_restaurant_list(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
    items_per_page: int = 10,
    page:int = 1
):
    url = f"{settings.RESTAURANT_BASE_API}/api/v1/restaurants/list"
    query_params = {
        "items_per_page":items_per_page,
        "page": page
    }
    response = requests.get(url, params=query_params)
    return response.json()

@router.get("/menu/{restaurant_id}")
async def get_restaurant_list(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    restaurant_id:UUID,
    current_user: CurrentUser,
    items_per_page: int = 10,
    page:int = 1
):
    url = f"{settings.RESTAURANT_BASE_API}/api/v1/menus/{restaurant_id}"
    query_params = {
        "items_per_page":items_per_page,
        "page": page
    }
    response = requests.get(url, params=query_params)
    return response.json()