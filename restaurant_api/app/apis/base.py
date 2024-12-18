from fastapi import APIRouter

from app.apis.v1 import route_login
from app.apis.v1 import route_user
from app.apis.v1 import route_restaurants
from app.apis.v1 import route_menu

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/login")
api_router.include_router(route_user.router, prefix="/user")
api_router.include_router(route_restaurants.router, prefix="/restaurants")
api_router.include_router(route_menu.router, prefix="/menus")

