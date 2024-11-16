from typing import Dict, Any, Literal, Union
from uuid import UUID

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.v1.db_restaurant import Restaurant
from app.schemas.v1.schema_restaurant import (
    RestaurantCreateInternal,
    RestaurantUpdate,
    RestaurantUpdateInternal,
    RestaurantDelete,
    RestaurantCreate,
    RestaurantRead,
    RestaurantReadOpen,
)

from app.core.http_exceptions import DuplicateValueException

from app.core.hashing import Hasher
from app.utils.paginated import (
    paginated_response,
    compute_offset,
)

# CRUD operations for the 'RestaurantRead' model
CRUDRestaurantRead = CRUDBase[
    Restaurant, RestaurantCreateInternal, RestaurantUpdate, RestaurantUpdateInternal, RestaurantDelete
]

# Create an instance of CRUDRestaurantRead for the 'RestaurantRead' model
crud_restaurants = CRUDRestaurantRead(Restaurant)


async def create_new_restaurant(restaurant: RestaurantCreate, db: AsyncSession) -> RestaurantRead:
    email_row = await crud_restaurants.exists(db=db, email=restaurant.email)
    if email_row:
        raise DuplicateValueException("Email is already registered")
    username_row = await crud_restaurants.exists(db=db, username=restaurant.username)
    if username_row:
        raise DuplicateValueException("Restaurant name not available")

    restaurant_internal_dict = restaurant.model_dump()
    restaurant_internal_dict["hashed_password"] = Hasher.get_hash_password(
        plain_password=restaurant_internal_dict["password"]
    )
    del restaurant_internal_dict["password"]

    restaurant_internal = RestaurantCreateInternal(**restaurant_internal_dict)
    return await crud_restaurants.create(db=db, object=restaurant_internal)


async def get_restaurant(
    username_or_email: str, db: AsyncSession
) -> Union[Dict[str, Any], Literal[None]]:
    if "@" in username_or_email:
        db_restaurant: dict = await crud_restaurants.get(
            db=db, email=username_or_email, is_deleted=False
        )
    else:
        db_restaurant = await crud_restaurants.get(
            db=db, username=username_or_email, is_deleted=False
        )

    if not db_restaurant:
        return None

    return db_restaurant

async def get_restaurant_byID(
    id: UUID, db: AsyncSession
) -> Union[Dict[str, Any], Literal[None]]:
    db_restaurant = await crud_restaurants.get(
            db=db, id=id, is_deleted=False
        )
    if not db_restaurant:
        return None

    return db_restaurant

async def get_restaurant_list(
    db: AsyncSession,
    page: int = 1,
    items_per_page: int = 10,
):
    restaurants_data = await crud_restaurants.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=RestaurantReadOpen,
            is_deleted=False,
            is_superuser=False
        )
    return paginated_response(
        crud_data=restaurants_data, page=page, items_per_page=items_per_page
    )