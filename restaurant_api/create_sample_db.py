def populate_sample_data(db: Session):
    # Sample restaurant
    restaurant = Restaurant(
        name="The Cozy Cafe",
        address="123 Elm Street",
        hours_of_operation="8:00 AM - 8:00 PM",
        owner_id=1  # assuming an owner ID for simplicity
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    # Sample menu items
    menu_items = [
        MenuItem(
            restaurant_id=restaurant.id,
            name="Pasta Primavera",
            description="Fresh pasta with seasonal vegetables",
            price=12.99,
            available=True
        ),
        MenuItem(
            restaurant_id=restaurant.id,
            name="Margherita Pizza",
            description="Classic pizza with fresh tomatoes and basil",
            price=10.99,
            available=True
        ),
        MenuItem(
            restaurant_id=restaurant.id,
            name="Caesar Salad",
            description="Crisp romaine lettuce with Caesar dressing",
            price=8.99,
            available=True
        )
    ]
    db.add_all(menu_items)
    db.commit()

    # Sample orders
    orders = [
        Order(
            restaurant_id=restaurant.id,
            status="pending"
        ),
        Order(
            restaurant_id=restaurant.id,
            status="preparing"
        ),
        Order(
            restaurant_id=restaurant.id,
            status="ready for delivery"
        )
    ]
    db.add_all(orders)
    db.commit()

    print("Sample data inserted successfully.")

# Populate sample data
populate_sample_data(db)
db.close()
