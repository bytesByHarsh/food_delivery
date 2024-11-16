# Built-in Dependencies
import random

# Third-Party Dependencies
from sqlmodel import select

# Local Dependencies
from app.db.session import AsyncSession, local_session
from app.db.session import async_engine as engine
from app.db.models.v1.common import Base

from app.core.config import settings
from app.core.hashing import Hasher
from app.db.models.v1.db_restaurant import Restaurant
from app.db.models.v1.db_menu import MenuItem, ItemAddOn



async def create_dummy_restaurant(session: AsyncSession) -> None:
    name = "Dummy Restaurant 1"
    email = "dummy1@gmail.com"
    username = "dummy1"
    phone = "+919876543213"
    hashed_pass = Hasher.get_hash_password("123")
    address = "123 Street, Jaipur"

    # check if already existing
    query = select(Restaurant).filter_by(email=email)
    result = await session.exec(query)
    user = result.one_or_none()

    if user is None:
        restaurant = Restaurant(
            name=name,
            email=email,
            username=username,
            phone=phone,
            hashed_password=hashed_pass,
            is_superuser=False,
            address=address,
            close_hr=24,
            open_hr=0,
            pincode=500081,
            latitude=17.433155,
            longitude=78.390158
        )
        session.add(
            restaurant
        )
        await session.commit()
        await create_dummy_menu(session=session, restaurant_id=restaurant.id)

    name = "Dummy Restaurant 2"
    email = "dummy2@gmail.com"
    username = "dummy2"
    phone = "+919876543218"
    hashed_pass = Hasher.get_hash_password("123")
    address = "123 Street, Jaipur"

    # check if already existing
    query = select(Restaurant).filter_by(email=email)
    result = await session.exec(query)
    user = result.one_or_none()

    if user is None:
        restaurant = Restaurant(
            name=name,
            email=email,
            username=username,
            phone=phone,
            hashed_password=hashed_pass,
            is_superuser=False,
            address=address,
            close_hr=24,
            open_hr=0,
            pincode=500081,
            latitude=17.433155,
            longitude=78.390158
        )
        session.add(
            restaurant
        )
        await session.commit()
        await create_dummy_menu(session=session, restaurant_id=restaurant.id)

async def create_dummy_menu(session: AsyncSession, restaurant_id) -> None:

    for i in range(random.randint(15, 20)):
        menu_item = MenuItem(
            available=random.choice([True, False]),
            description=f"Item Description {i + 1}",
            name=f"Item {i + 1}",
            price=random.uniform(56, 450),
            restaurant_id=restaurant_id,
        )
        session.add(menu_item)
        await session.commit()

        add_ons = []
        for j in range(random.randint(0, 5)):
            add_on = ItemAddOn(
                available=random.choice([True, False]),
                description=f"Add On Description {j + 1}",
                name=f"Add On {j + 1}",
                price=random.uniform(5, 50),
                item_id=menu_item.id
            )
            add_ons.append(add_on)
        if len(add_ons):
            session.add_all(add_ons)
            await session.commit()