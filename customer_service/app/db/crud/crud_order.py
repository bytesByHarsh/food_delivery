from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.schemas.v1.schema_user import UserRead
from app.db.models.v1.db_order import Order, OrderItem, OrderAddOn, Order_Status_Enum
from app.schemas.v1.schema_order import (
    OrderCreateInternal,
    OrderUpdate,
    OrderUpdateInternal,
    OrderDelete,
    OrderCreate,
    OrderRead,
    OrderItemCreateInternal,
    OrderItemUpdate,
    OrderItemUpdateInternal,
    OrderItemDelete,
    OrderItemRead,
    OrderAddOnCreateInternal,
    OrderAddOnUpdate,
    OrderAddOnUpdateInternal,
    OrderAddOnDelete,
    OrderAddOnRead,
    OrderUpdateDriverDetails,
)
from app.core.http_exceptions import ForbiddenException

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


async def add_new_order(user: UserRead, order: OrderCreate, db: AsyncSession):
    order_c = OrderCreateInternal(
        customer_id=order.customer_id,
        address_id=order.address_id,
        restaurant_id=order.restaurant_id,
        total_cost=0.0,
    )

    order_db = await crud_order.create(db=db, object=order_c)
    total_price: float = 0
    ## parse orders items
    for item in order.items:
        item_c = OrderItemCreateInternal(order_id=order_db.id, **item.model_dump())
        item_db = await crud_orderItem.create(db=db, object=item_c)
        for add_on in item.add_ons:
            add_on_c = OrderAddOnCreateInternal(
                order_item_id=item_db.id,
                name=add_on.name,
                price=add_on.price,
            )
            total_price += add_on.price
            await crud_orderAddOn.create(db=db, object=add_on_c)
        total_price += item.price_per_unit * item.quantity
    order_db.total_cost = total_price
    await crud_order.update(db=db, object=order_db, id=order_db.id)  # type:ignore
    return order_db


async def get_order_details(
    order_id: UUID,
    db: AsyncSession,
):
    order_db = await crud_order.get(db=db, id=order_id)

    items = await crud_orderItem.get_multi(
        db=db,
        limit=100,
        offset=0,
        is_deleted=False,
        schema_to_select=OrderItemRead,
        order_id=order_db["id"],
    )
    items = items["data"]
    for item in items:
        add_ons = await crud_orderAddOn.get_multi(
            db=db,
            limit=100,
            offset=0,
            is_deleted=False,
            schema_to_select=OrderAddOnRead,
            order_item_id=item["id"],  # type:ignore
        )
        add_ons = add_ons["data"]
        item["add_ons"] = add_ons  # type:ignore
    order_db["items"] = items

    return order_db


async def get_order_list(
    user: UserRead,
    db: AsyncSession,
    page: int = 1,
    items_per_page: int = 10,
):
    order_data = await crud_order.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=OrderRead,
        is_deleted=False,
        customer_id=user.id,
    )
    return paginated_response(
        crud_data=order_data, page=page, items_per_page=items_per_page
    )


async def update_order_status(
    order_id: UUID,
    status: Order_Status_Enum,
    db: AsyncSession,
    customer_id: UUID | None = None,
    restaurant_id: str | None = None,
    driver_id: str | None = None,
):
    order_db = await crud_order.get(db=db, id=order_id)
    check_fag: bool = False
    if customer_id is not None:
        check_fag = True
        if order_db["customer_id"] != customer_id:
            raise ForbiddenException("Different Customer Trying to update order status")

    if restaurant_id is not None:
        check_fag = True
        if order_db["restaurant_id"] != restaurant_id:
            raise ForbiddenException(
                "Different Restaurant Trying to update order status"
            )

    if driver_id is not None:
        check_fag = True
        if order_db["delivery_person_id"] != int(driver_id):
            raise ForbiddenException("Different Driver Trying to update order status")
    if check_fag is False:
        raise ForbiddenException("Wrong Params Entered")
    order_db["status"] = status
    await crud_order.update(db=db, object=order_db, id=order_id)
    return True

async def update_driver(
    order_id: UUID,
    driver_details: OrderUpdateDriverDetails,
    db: AsyncSession,
):
    await crud_order.update(db=db, object=driver_details, id=order_id)
