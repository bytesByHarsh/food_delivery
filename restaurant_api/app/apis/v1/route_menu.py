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
from app.core.dependencies import CurrentUser, CurrentSuperUser

from app.schemas.v1.schema_menu import (
    MenuItemRead,
    MenuItemCreate,
    ItemAddOnRead,
    ItemAddOnCreate
)
from app.utils.paginated import PaginatedListResponse
from app.db.session import async_get_db

from app.db.crud.crud_menu import add_item_in_menu, get_restaurant_menu

router = APIRouter(tags=["Menu Management"])

@router.post("/create")
async def create_restaurant(
    request: Request,
    menu_item: MenuItemCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    restaurant: CurrentUser,
):
    return await add_item_in_menu(db=db, restaurant=restaurant, menu_item=menu_item)

@router.get("/{restaurant_id}")
async def create_restaurant(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    restaurant_id:UUID,
    page: int = 1,
    items_per_page: int = 10,
):
    return await get_restaurant_menu(
        db=db,
        restaurant_id=restaurant_id,
        page=page,
        items_per_page=items_per_page
    )