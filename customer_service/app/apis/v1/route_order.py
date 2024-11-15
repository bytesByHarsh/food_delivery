# Built-in Dependencies
from typing import Annotated, Any
from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request
import fastapi

# Local Dependencies
from app.core.dependencies import CurrentUser
from app.db.crud.crud_order import (
    add_new_order,
    update_order_status,
    get_order_details,
    get_order_list,
    update_driver,
)
from app.db.session import async_get_db
from app.schemas.v1.schema_order import OrderCreate, OrderRead, OrderUpdateDriverDetails

from app.db.models.v1.db_order import Order_Status_Enum
from app.utils.paginated import (
    PaginatedListResponse,
)

router = fastapi.APIRouter(tags=["Orders"])


@router.post("", response_model=OrderRead, status_code=201)
async def create_order(
    request: Request,
    order: OrderCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
) -> Any:
    return await add_new_order(user=current_user, order=order, db=db)


@router.get("/list", response_model=PaginatedListResponse[OrderRead])
async def order_list(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
    page: int = 1,
    items_per_page: int = 10,
):
    return await get_order_list(
        db=db, items_per_page=items_per_page, page=page, user=current_user
    )


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    request: Request, order_id: UUID, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    return await get_order_details(db=db, order_id=order_id)


@router.put("{order_id}", status_code=200)
async def update_status(
    request: Request,
    order_id: UUID,
    status: Order_Status_Enum,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    restaurant_id: str | None = None,
    customer_id: UUID | None = None,
    driver_id: str | None = None,
):
    status = await update_order_status(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        driver_id=driver_id,
        order_id=order_id,
        status=status,
        db=db,
    )

    if status:
        return {"status": "Updated"}
    return {"status": "Not Updated, Check value sent"}

@router.post("/{order_id}/assign", response_model=OrderRead, status_code=200)
async def create_order(
    request: Request,
    order_id: UUID,
    driver_details:OrderUpdateDriverDetails,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Any:
    return await update_driver(db=db, driver_details=driver_details, order_id=order_id)
