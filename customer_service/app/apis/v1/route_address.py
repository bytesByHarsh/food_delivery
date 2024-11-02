# Built-in Dependencies
from typing import Annotated, Dict, Any
from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request
import fastapi

# Local Dependencies
from app.core.dependencies import CurrentUser, CurrentSuperUser
from app.db.session import async_get_db
from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
)

from app.schemas.v1.schema_address import (
    UserAddressCreate,
    UserAddressRead,
    UserAddressUpdate
)

from app.utils.paginated import (
    PaginatedListResponse,
    paginated_response,
    compute_offset,
)
from app.core.config import settings

from app.db.crud.crud_user_address import (
    add_new_address,
    get_address_details,
    get_address_list_details,
    remove_address
)

router = fastapi.APIRouter(tags=["User Address"])


@router.post("", response_model=UserAddressRead, status_code=201)
async def add_address(
    request: Request,
    address:UserAddressCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
):
    if current_user.id != address.customer_id:
        raise ForbiddenException("Cannot add address for different user")
    return await add_new_address(user=current_user, address=address, db=db)

@router.get("/{address_id}", response_model=UserAddressRead, status_code=200)
async def get_address(
    request: Request,
    address_id:UUID,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
):
    return await get_address_details(user=current_user, id=address_id, db=db)

@router.get("", status_code=200, response_model= PaginatedListResponse[UserAddressRead])
async def get_address_list(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
    page: int = 1,
    items_per_page: int = 10,
):
    return await get_address_list_details(user=current_user, db=db, page=page, items_per_page=items_per_page)


@router.delete("/{address_id}")
async def delete_address(
    request: Request,
    address_id:UUID,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
):
    status = await remove_address(db=db, id=address_id, user=current_user)
    if status:
        return "Address Deleted"
    return "Address Not deleted"