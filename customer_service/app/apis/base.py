from fastapi import APIRouter

from app.apis.v1 import route_login
from app.apis.v1 import route_user
from app.apis.v1 import route_address
from app.apis.v1 import route_order

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/auth", tags=["Login"])
api_router.include_router(route_user.router, prefix="/users", tags=["Users"])
api_router.include_router(
    route_address.router, prefix="/user_address", tags=["User Address"]
)
api_router.include_router(route_order.router, prefix="/orders")
