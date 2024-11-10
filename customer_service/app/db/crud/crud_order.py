from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.schemas.v1.schema_user import UserRead
from app.db.models.v1.db_order import (
    Order,
    OrderItem,
    OrderAddOn
)
from app.schemas.v1.schema_order import (
    OrderCreateInternal,
    OrderUpdate,
    OrderUpdateInternal,
    OrderDelete,
    OrderCreate,

    OrderItemCreateInternal,
    OrderItemUpdate,
    OrderItemUpdateInternal,
    OrderItemDelete,
    OrderItemCreate,

    OrderAddOnCreateInternal,
    OrderAddOnUpdate,
    OrderAddOnUpdateInternal,
    OrderAddOnDelete,
    OrderAddOnCreate,
)
from app.core.http_exceptions import NotFoundException, ForbiddenException

from app.utils.paginated import (
    paginated_response,
    compute_offset,
)


# CRUD operations for the 'Order' model
CRUDOrder = CRUDBase[
    Order,
    OrderCreateInternal,
    OrderUpdate,
    OrderUpdateInternal,
    OrderDelete,
]

# Create an instance of CRUDUser for the 'Order' model
crud_order = CRUDOrder(Order)

# CRUD operations for the 'OrderItem' model
CRUDOrderItem = CRUDBase[
    OrderItem,
    OrderItemCreateInternal,
    OrderItemUpdate,
    OrderItemUpdateInternal,
    OrderItemDelete,
]

# Create an instance of CRUDUser for the 'OrderItem' model
crud_orderItem = CRUDOrderItem(OrderItem)

# CRUD operations for the 'OrderAddOn' model
CRUDOrderAddOn = CRUDBase[
    OrderAddOn,
    OrderAddOnCreateInternal,
    OrderAddOnUpdate,
    OrderAddOnUpdateInternal,
    OrderAddOnDelete,
]

# Create an instance of CRUDUser for the 'OrderAddOn' model
crud_orderAddOn = CRUDOrderAddOn(OrderAddOn)


async def add_new_order(
    user: UserRead,
    order: OrderCreate,
    db: AsyncSession
):
    print(order)