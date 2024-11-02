from typing import Dict, Any, Literal, Union
from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.schemas.v1.schema_user import UserRead
from app.db.models.v1.db_address import UserAddress
from app.schemas.v1.schema_address import (
    UserAddressCreateInternal,
    UserAddressUpdate,
    UserAddressUpdateInternal,
    UserAddressDelete,
    UserAddressCreate,
    UserAddressRead
)
from app.core.http_exceptions import (
    NotFoundException,
    ForbiddenException
)

from app.utils.paginated import (
    paginated_response,
    compute_offset,
)


# CRUD operations for the 'UserAddress' model
CRUDUserAddress = CRUDBase[
    UserAddress, UserAddressCreateInternal, UserAddressUpdate, UserAddressUpdateInternal, UserAddressDelete
]

# Create an instance of CRUDUser for the 'UserAddress' model
crud_userAddress = CRUDUserAddress(UserAddress)

async def add_new_address(user:UserRead, address: UserAddressCreate, db: AsyncSession) -> UserAddress:
    address.customer_id = user.id

    data_internal = UserAddressCreateInternal(**address.model_dump())
    return await crud_userAddress.create(db=db, object=data_internal)

async def get_address_details(user:UserRead, id:UUID, db: AsyncSession) -> UserAddress:
    address = await crud_userAddress.get(db=db, schema_to_select=UserAddress, id=id, customer_id=user.id)
    if not address:
        return NotFoundException("Address ID not found")
    if address["customer_id"] != user.id:
        return ForbiddenException("User does not have permission to delete this address")
    return address

async def get_address_list_details(
    user:UserRead,
    db: AsyncSession,
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    address_data = await crud_userAddress.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=UserAddressRead,
            is_deleted=False,
        )
    return paginated_response(
        crud_data=address_data, page=page, items_per_page=items_per_page
    )

async def remove_address(user: UserRead, id:UUID, db: AsyncSession):
    try:
        address = await get_address_details(user, id, db)
        await crud_userAddress.delete(db=db,  db_row=address, id=id)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

async def update_address(user: UserRead, address:UserAddressUpdate, db: AsyncSession):
    pass
