from fastapi import APIRouter

from app.apis.v1 import route_restaurant

api_router = APIRouter()

api_router.include_router(route_restaurant.router, prefix="/restaurants")

