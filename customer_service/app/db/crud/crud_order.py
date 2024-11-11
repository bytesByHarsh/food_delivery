from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.schemas.v1.schema_user import UserRead
from app.db.models.v1.db_order import (
    Order,
    OrderItem,
    OrderAddOn,
    Order_Status_Enum
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

    order_c  = OrderCreateInternal(
        customer_id=order.customer_id,
        address_id=order.address_id,
        restaurant_id=order.restaurant_id,
    )

    order_db = await crud_order.create(db=db, object=order_c)

    ## parse orders items
    for item in order.items:
        item_c = OrderItemCreateInternal(order_id=order_db.id,**item.model_dump())
        item_db = await crud_orderItem.create(db=db, object=item_c)
        for add_on in item.add_ons:
            add_on_c = OrderAddOnCreateInternal(
                order_item_id= item_db.id,
                name=add_on.name,
                price=add_on.price,
            )
            await crud_orderAddOn.create(db=db, object=add_on_c)
    return order_db


async def update_order_status(
    user_id: UUID | None,
    restaurant_id,
    driver_id,
    order_id: UUID,
    db: AsyncSession
):
    order_db = await crud_order.get(db=db, id=order_id)

    # if user_id is not None:
    #     if order_db.us
