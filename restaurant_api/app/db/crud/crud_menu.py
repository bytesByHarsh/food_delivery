from typing import Dict, Any, Literal, Union
from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.v1.db_menu import MenuItem, ItemAddOn
from app.schemas.v1.schema_restaurant import RestaurantRead
from app.core.http_exceptions import DuplicateValueException

from app.schemas.v1.schema_menu import (
    ItemAddOnCreateInternal,
    ItemAddOnUpdate,
    ItemAddOnUpdateInternal,
    ItemAddOnDelete,
    ItemAddOnCreate,
    ItemAddOnRead,

    MenuItemCreateInternal,
    MenuItemUpdate,
    MenuItemUpdateInternal,
    MenuItemDelete,
    MenuItemCreate,
    MenuItemRead,
)
from app.utils.paginated import (
    paginated_response,
    compute_offset,
)

# CRUD operations for the 'MenuItemRead' model
CRUDMenuItemRead = CRUDBase[
    MenuItem, MenuItemCreateInternal, MenuItemUpdate, MenuItemUpdateInternal, MenuItemDelete
]

# Create an instance of CRUDMenuItemRead for the 'MenuItemRead' model
crud_menu_items = CRUDMenuItemRead(MenuItem)

# CRUD operations for the 'ItemAddOnRead' model
CRUDItemAddOnRead = CRUDBase[
    ItemAddOn, ItemAddOnCreateInternal, ItemAddOnUpdate, ItemAddOnUpdateInternal, ItemAddOnDelete
]

# Create an instance of CRUDItemAddOnRead for the 'ItemAddOnRead' model
crud_item_add_on = CRUDItemAddOnRead(ItemAddOn)

async def add_item_in_menu(
    menu_item: MenuItemCreate,
    restaurant: RestaurantRead,
    db: AsyncSession
):
    pass

async def get_restaurant_menu(
    restaurant_id: UUID,
    db: AsyncSession,
    page: int = 1,
    items_per_page: int = 10,
):
    menu_items = await crud_menu_items.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=MenuItemRead,
        is_deleted=False,
    )
    for item in menu_items["data"]:
        add_ons = await crud_item_add_on.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=ItemAddOnRead,
            item_id=item["id"],
            is_deleted=False,
        )
        item["add_ons"] = add_ons["data"]
    return paginated_response(
        crud_data=menu_items, page=page, items_per_page=items_per_page
    )