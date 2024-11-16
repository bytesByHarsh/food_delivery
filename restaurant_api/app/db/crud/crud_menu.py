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